# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Handles interacting with Google Ads API."""
from __future__ import annotations

from collections.abc import Sequence

import gaarf
import numpy as np

from googleads_housekeeper.domain.core import exclusion_specification
from googleads_housekeeper.domain.core import task
from googleads_housekeeper.domain.placement_handler import entities
from googleads_housekeeper.services import enums


class PlacementFetcher:
    """Handles fetching of placement data from Google Ads API.

    Attributes:
        report_fetcher: An instance of AdsReportFetcher to handle API requests.
    """

    def __init__(self,
                 report_fetcher: gaarf.query_executor.AdsReportFetcher) -> None:
        """Initializes PlacementFetcher.

        Args:
            report_fetcher:
                An instance of AdsReportFetcher to handle API requests.
        """
        self.report_fetcher = report_fetcher

    def get_placements_for_account(
        self,
        account: str,
        task_obj: task.Task,
    ) -> gaarf.report.GaarfReport | None:
        """Gets placement data from a given account based on task definition.

        Args:
            account: Google Ads account to get data from.
            task_obj: A task defining parameters of fetching.
        Returns:
            Report with fetched placement data.
        """
        specification = (
            exclusion_specification.ExclusionSpecification.from_expression(
                task_obj.exclusion_rule))
        runtime_options = specification.define_runtime_options()
        if not (placements := self._get_placement_performance_data(
                account, task_obj)):
            return None
        if runtime_options.is_conversion_query and (
                placements_by_conversion_name :=
                self._get_placement_conversion_split_data(account, task_obj)):
            conversion_split_exclusion_specification = (
                exclusion_specification.ExclusionSpecification(
                    specifications=[runtime_options.conversion_rules]))
            placements_by_conversion_name = (
                conversion_split_exclusion_specification.apply_specifications(
                    placements_by_conversion_name))
            placements = self._join_conversion_split(
                placements, placements_by_conversion_name,
                runtime_options.conversion_name)
        return self._aggregate_placements(placements, task_obj.exclusion_level)

    def _get_placement_performance_data(
            self, account: str,
            task_obj: task.Task) -> gaarf.report.GaarfReport:
        """Gets placement performance data (clicks, impressions, etc.).

        Args:
            account: Google Ads account to get data from.
            task_obj: A task defining parameters of fetching.
        Returns:
            Report with fetched placement data.
        """
        placements = self._get_placement_data(
            task_obj=task_obj, account=account)
        if 'YOUTUBE_VIDEO' in task_obj.placement_types:
            if (detail_placements := self._get_placement_data(
                    task_obj=task_obj,
                    account=account,
                    placement_level_granularity='detail_placement_view')):
                placements = placements + detail_placements
        return placements

    def _get_placement_conversion_split_data(
            self, account: str,
            task_obj: task.Task) -> gaarf.report.GaarfReport:
        """Gets placement conversion split data (conversion_name, conversions).

        Args:
            account: Google Ads account to get data from.
            task_obj: A task defining parameters of fetching.
        Returns:
            Report with fetched placement conversion split data.
        """
        placements = self._get_placement_data(
            task_obj=task_obj,
            account=account,
            query_class=entities.PlacementsConversionSplit)
        if 'YOUTUBE_VIDEO' in task_obj.placement_types:
            if (detail_placements := self._get_placement_data(
                    task_obj=task_obj,
                    account=account,
                    query_class=entities.PlacementsConversionSplit)):
                placements = placements + detail_placements
        return placements

    def get_already_excluded_placements(
            self, account: str,
            exclusion_level: enums.ExclusionLevelEnum) -> dict[str, list[str]]:
        """Fetches negative placement criteria from Google Ads account.

        Negative criteria are fetched based on specified exclusion level (
        ACCOUNT, CAMPAIGN, AD_GROUP).

        Args:
            account: Google Ads account to get data from.
            exclusion_level: Level of exclusion (ACCOUNT, CAMPAIGN, AD_GROUP).
        Returns:
            Mapping between entity_id from specified exclusion level to all
            negative criteria ids.
        """
        already_excluded_placements = self.report_fetcher.fetch(
            entities.AlreadyExcludedPlacements(exclusion_level), account)
        if not already_excluded_placements:
            return {}
        for row in already_excluded_placements:
            row['placement'] = (
                row.website_url or row.app_id or row.video_id or
                row.channel_id or '')
        return already_excluded_placements.to_dict(
            key_column='level_id',
            value_column='placement',
            value_column_output='list')

    def get_placement_exclusion_lists(
            self, customer_ids: Sequence[int]) -> dict[str, str]:

        placement_exclusion_lists = self.report_fetcher.fetch(
            entities.PlacementExclusionLists(), customer_ids)
        return placement_exclusion_lists.to_dict(
            key_column='name',
            value_column='resource_name',
            value_column_output='scalar')

    def _get_placement_data(
        self,
        task_obj: task.Task,
        account: str,
        query_class: gaarf.base_query.BaseQuery = entities.Placements,
        placement_level_granularity: str = 'group_placement_view'
    ) -> gaarf.report.Report:
        """Helper method for building query and fetching data from Ads API.

        Args:
            task_obj: A Task that contains necessary data for building query.
            account: Google Ads account to fetch data from.
            query_class: Class defining which query will be built.
            placement_level_granularity: Resource name to get data from.
        Returns:
            Report containing placement performance data.
        """
        placement_query = query_class(
            placement_types=task_obj.placement_types,
            placement_level_granularity=placement_level_granularity,
            start_date=task_obj.start_date,
            end_date=task_obj.end_date)
        return self.report_fetcher.fetch(placement_query, customer_ids=account)

    def _join_conversion_split(
            self, placements: gaarf.report.GaarfReport,
            placements_by_conversion_name: gaarf.report.GaarfReport,
            conversion_name: str) -> gaarf.report.GaarfReport:
        """Joins placements performance data with its conversion split data.

        Args:
            placements:
                Report with placement performance data.
            placements_by_conversion_name:
                Report with placements conversion split data.
            conversion_name:
                Conversion_name(s) that should be used to create a dedicated
                column in joined report.

        Returns:
            New report with extra conversion specific columns.
        """
        conversion_names = conversion_name.replace('"', '').split(',')
        placements_by_conversion_name = placements_by_conversion_name.to_pandas(
        )
        final_report_values = []
        for row in placements:
            is_conversion_row = (
                placements_by_conversion_name.ad_group_id == row.ad_group_id
            ) & (placements_by_conversion_name.placement == row.placement) & (
                placements_by_conversion_name.conversion_name.isin(
                    conversion_names))
            conversion_row = placements_by_conversion_name.loc[
                is_conversion_row]
            data = list(row.data)
            if not (conversions := sum(conversion_row['conversions'].values)):
                conversions = 0.0
            if not (all_conversions := sum(
                    conversion_row['all_conversions'].values)):
                all_conversions = 0.0
            data.extend([conversion_name, conversions, all_conversions])
            final_report_values.append(data)
        columns = list(placements.column_names)
        columns.extend(['conversion_name', 'conversions_', 'all_conversions_'])
        return gaarf.report.GaarfReport(
            results=final_report_values, column_names=columns)

    def _aggregate_placements(
            self,
            placements: gaarf.report.GaarfReport,
            exclusion_level: str | enums.ExclusionLevelEnum,
            perform_relative_aggregations: bool = True
    ) -> gaarf.report.GaarfReport:
        """Aggregates placements to a desired exclusion_level.

        By default Placements report returned on Ad Group level, however exclusion
        can be performed on Campaign, Account and MCC level. By aggregating report
        to a desired level exclusion specification can be property applied to
        identify placements that should be excluded.

        Args:
            placements:
                Report with placement related metrics.
            exclusion_level:
                Desired level of aggregation.
            perform_relative_aggregations:
                Whether or not calculate relative metrics (CTR, CPC, etc.)
        Returns:
            Updated report aggregated to desired exclusion level.
        """
        if not isinstance(exclusion_level, enums.ExclusionLevelEnum):
            exclusion_level = getattr(enums.ExclusionLevelEnum, exclusion_level)
        base_groupby = [
            'placement', 'placement_type', 'name', 'criterion_id', 'url'
        ]
        aggregation_dict = dict.fromkeys([
            'clicks',
            'impressions',
            'cost',
            'conversions',
            'video_views',
            'interactions',
            'all_conversions',
            'view_through_conversions',
        ], 'sum')
        relative_aggregations_dict = {
            'ctr': ['clicks', 'impressions'],
            'avg_cpc': ['cost', 'clicks'],
            'avg_cpm': ['cost', 'impressions'],
            'avg_cpv': ['cost', 'video_views'],
            'video_view_rate': ['video_views', 'impressions'],
            'interaction_rate': ['interactions', 'clicks'],
            'conversions_from_interactions_rate': [
                'conversions', 'interactions'
            ],
            'cost_per_conversion': ['cost', 'conversions'],
            'cost_per_all_conversion': ['cost', 'all_conversions'],
            'all_conversion_rate': ['all_conversions', 'interactions'],
            'all_conversions_from_interactions_rate': [
                'all_conversions', 'interactions'
            ],
        }
        if 'conversion_name' in placements.column_names:
            base_groupby = base_groupby + ['conversion_name']
            aggregation_dict.update(
                dict.fromkeys(['conversions_', 'all_conversions_'], 'sum'))
            relative_aggregations_dict.update({
                'cost_per_conversion_': ['cost', 'conversions_'],
                'cost_per_all_conversion_': ['cost', 'all_conversions_']
            })

        aggregation_groupby = self._define_aggregation_group_by(exclusion_level)
        groupby = [
            base for base in base_groupby + aggregation_groupby
            if base in placements.column_names
        ]
        aggregations = {
            key: value
            for key, value in aggregation_dict.items()
            if key in placements.column_names
        }
        aggregated_placements = placements.to_pandas().groupby(
            groupby, as_index=False).agg(aggregations)
        if perform_relative_aggregations:
            for key, [numerator,
                      denominator] in relative_aggregations_dict.items():
                if set([numerator, denominator
                       ]).issubset(set(aggregated_placements.columns)):
                    aggregated_placements[key] = aggregated_placements[
                        numerator] / aggregated_placements[denominator]
                    if key == 'avg_cpm':
                        aggregated_placements[
                            key] = aggregated_placements[key] * 1000
                    if key == 'ctr':
                        aggregated_placements[key] = round(
                            aggregated_placements[key], 4)
                    else:
                        aggregated_placements[key] = round(
                            aggregated_placements[key], 2)
        aggregated_placements.replace([np.inf, -np.inf], 0, inplace=True)
        return gaarf.report.GaarfReport.from_pandas(aggregated_placements)

    def _define_aggregation_group_by(
            self, exclusion_level: enums.ExclusionLevelEnum) -> list[str]:
        aggregation_groupby = ['account_name', 'customer_id']
        if exclusion_level == enums.ExclusionLevelEnum.CAMPAIGN:
            aggregation_groupby += [
                'campaign_id', 'campaign_name', 'campaign_type'
            ]
        elif exclusion_level == enums.ExclusionLevelEnum.AD_GROUP:
            aggregation_groupby += [
                'campaign_id', 'campaign_name', 'campaign_type', 'ad_group_id',
                'ad_group_name'
            ]
        return aggregation_groupby
