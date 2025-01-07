import json
from datetime import datetime, timezone, timedelta
import logging
from typing import Dict

from leetcode_cli.graphics.ansi_codes import ANSI_CODES
from leetcode_cli.exceptions.exceptions import StatsError

logger = logging.getLogger(__name__)


class StatsManager:
    """
    Manages statistics-related functionalities, including processing user activity and statistics.
    """

    def join_and_slice_calendars(self, previous_year_calendar: Dict, current_year_calendar: Dict) -> Dict[int, int]:
        """
        Joins, merges, and slices LeetCode user calendar data from two years.

        Args:
            previous_year_calendar (Dict): Calendar data from the previous year.
            current_year_calendar (Dict): Calendar data from the current year.

        Returns:
            Dict[int, int]: Merged and sliced calendar data with timestamps as keys and submission counts as values.

        Raises:
            StatsError: If calendar data is missing or malformed.
        """
        if not previous_year_calendar or not current_year_calendar:
            logger.error("Missing previous or current year calendar data.")
            raise StatsError("Missing previous or current year calendar data.")

        try:
            prev_data = json.loads(previous_year_calendar['data']['matchedUser']['userCalendar']['submissionCalendar'])
            curr_data = json.loads(current_year_calendar['data']['matchedUser']['userCalendar']['submissionCalendar'])
        except KeyError as e:
            logger.error(f"Missing key in userCalendar: {e}")
            raise StatsError(f"Missing key in userCalendar: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decoding error: {e}")
            raise StatsError(f"JSON decoding error: {e}")

        merged = {**prev_data, **curr_data}
        # Convert keys to int timestamps
        merged = {int(k): v for k, v in merged.items()}

        today_utc = datetime.utcnow().date()
        start_date = today_utc - timedelta(days=365)
        start_dt = datetime.combine(start_date, datetime.min.time(), tzinfo=timezone.utc)
        end_dt = datetime.combine(today_utc, datetime.min.time(), tzinfo=timezone.utc)
        start_ts, end_ts = int(start_dt.timestamp()), int(end_dt.timestamp())

        # Slice to last year
        sliced = {ts: cnt for ts, cnt in merged.items() if start_ts <= ts < end_ts}
        logger.debug(f"Sliced calendar data from {start_date} to {today_utc}.")

        return sliced

    def fill_daily_activity(self, daily_activity: Dict[int, int]) -> Dict[int, int]:
        """
        Ensures every day in the last year is present in daily_activity, even if 0.

        Args:
            daily_activity (Dict[int, int]): Existing daily activity data.

        Returns:
            Dict[int, int]: Completed daily activity data with no missing days.
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

        logger.debug("Filled daily activity data with missing days set to 0.")
        return filled

    def calculate_color(self, submissions: int, max_submissions: int, min_submissions: int) -> str:
        """
        Calculates an ANSI color code for a day’s submission count relative to min/max in the data.

        Args:
            submissions (int): Number of submissions on a given day.
            max_submissions (int): Maximum submissions in the dataset.
            min_submissions (int): Minimum submissions in the dataset.

        Returns:
            str: ANSI color code.
        """
        CUSTOM_GREENS = [
            ANSI_CODES["green1"],
            ANSI_CODES["green2"],
            ANSI_CODES["green3"],
            ANSI_CODES["green4"],
            ANSI_CODES["green5"],
            ANSI_CODES["green6"]
        ]
        if max_submissions == min_submissions:
            return CUSTOM_GREENS[-1]

        normalized = (submissions - min_submissions) / (max_submissions - min_submissions)
        normalized = max(0.0, min(1.0, normalized))
        index = int(normalized * (len(CUSTOM_GREENS) - 1))
        color = CUSTOM_GREENS[index]
        logger.debug(f"Calculated color '{color}' for submissions count '{submissions}'.")
        return color
