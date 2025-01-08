# file: leetcode_cli/managers/stats_manager.py

import json
from datetime import datetime, timezone, timedelta
import logging
from typing import Dict

from leetcode_cli.managers.auth_service import AuthService
from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.exceptions.exceptions import FetchingError, StatsError, ParsingError
from leetcode_cli.parsers.stats_data_parser import (
    parse_user_stats_data,
    parse_single_year_calendar
)
from leetcode_cli.models.stats import UserStatsModel, UserActivityModel

from leetcode_cli.data_fetchers.stats_data_fetcher import (
    fetch_user_stats,
    fetch_user_activity
)

logger = logging.getLogger(__name__)

class StatsManager:
    """
    Manages statistics fetch + parse, plus the logic to join/fill user activity.
    The commands call these manager methods, then pass results to a formatter.
    """

    def __init__(self, config_manager: ConfigManager, auth_service: AuthService):
        self.config_manager = config_manager
        self.auth_service = auth_service

    #
    # ──────────────────────────────────────────────────────
    #   PUBLIC METHODS
    # ──────────────────────────────────────────────────────
    #

    def get_user_stats(self, username: str) -> UserStatsModel:
        """
        Fetch + parse user stats from LeetCode, returning a UserStatsModel.
        """
        try:
            raw = fetch_user_stats(username)
            return parse_user_stats_data(raw)
        except (FetchingError, ParsingError) as e:
            logger.error(f"Failed to get_user_stats: {e}")
            raise StatsError(str(e))

    def get_joined_activity(self, username: str, prev_year: int, curr_year: int) -> UserActivityModel:
        """
        Fetch raw calendar data for two years, parse them, then join + slice + fill to produce a final UserActivityModel.
        """
        try:
            # 1) fetch for each year
            raw_prev = fetch_user_activity(username, prev_year)
            raw_curr = fetch_user_activity(username, curr_year)
            # 2) parse each
            prev_dict = parse_single_year_calendar(raw_prev)  # Dict[int, int]
            curr_dict = parse_single_year_calendar(raw_curr)  # Dict[int, int]

            # 3) merge + slice + fill
            joined = self._join_and_slice_calendars(prev_dict, curr_dict)
            filled = self._fill_daily_activity(joined)

            # 4) return final model
            return UserActivityModel(daily_activity=filled)

        except (FetchingError, ParsingError) as e:
            logger.error(f"Failed to get_joined_activity: {e}")
            raise StatsError(str(e))

    #
    # ──────────────────────────────────────────────────────
    #   PRIVATE HELPERS
    # ──────────────────────────────────────────────────────
    #

    def _join_and_slice_calendars(
        self, prev_data: Dict[int, int], curr_data: Dict[int, int]
    ) -> Dict[int, int]:
        """
        Merges two dicts of {timestamp -> submissionCount}, then slices to the last 365 days.
        """
        merged = {**prev_data, **curr_data}

        today_utc = datetime.utcnow().date()
        start_date = today_utc - timedelta(days=365)
        start_dt = datetime.combine(start_date, datetime.min.time(), tzinfo=timezone.utc)
        end_dt = datetime.combine(today_utc, datetime.min.time(), tzinfo=timezone.utc)

        start_ts = int(start_dt.timestamp())
        end_ts = int(end_dt.timestamp())

        # slice
        sliced = {
            ts: cnt
            for ts, cnt in merged.items()
            if start_ts <= ts < end_ts
        }
        logger.debug(f"Sliced calendar data from {start_date} to {today_utc}, total {len(sliced)} days.")
        return sliced

    def _fill_daily_activity(self, daily_activity: Dict[int, int]) -> Dict[int, int]:
        """
        Ensures every day in the last year is present, even if 0 submissions.
        """
        filled = {}
        today_utc = datetime.utcnow().date()
        start_date = today_utc - timedelta(days=365)

        start_dt = datetime.combine(start_date, datetime.min.time(), tzinfo=timezone.utc)
        end_dt = datetime.combine(today_utc, datetime.min.time(), tzinfo=timezone.utc)

        current = start_dt
        while current <= end_dt:
            ts = int(current.timestamp())
            filled[ts] = daily_activity.get(ts, 0)
            current += timedelta(days=1)

        logger.debug(f"Filled missing days from {start_date} to {today_utc}, total {len(filled)} days.")
        return filled
