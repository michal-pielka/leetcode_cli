import json
from datetime import datetime, timezone, timedelta
import logging
from leetcode_cli.graphics.ansi_codes import ANSI_CODES

logger = logging.getLogger(__name__)

def join_and_slice_calendars(previous_year_calendar: dict, current_year_calendar: dict) -> dict:
    """
    Joins, merges, and slices LeetCode user calendar data from two years.
    """
    if not previous_year_calendar or not current_year_calendar:
        raise ValueError("Missing previous or current year calendar data.")

    try:
        prev_data = json.loads(previous_year_calendar['data']['matchedUser']['userCalendar']['submissionCalendar'])
        curr_data = json.loads(current_year_calendar['data']['matchedUser']['userCalendar']['submissionCalendar'])
    except KeyError as e:
        logger.error(f"Missing key in userCalendar: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"JSON decoding error: {e}")
        raise

    merged = {**prev_data, **curr_data}
    # Convert keys to int timestamps
    merged = {int(k): v for k, v in merged.items()}

    today_utc = datetime.utcnow().date()
    start_date = today_utc - timedelta(days=365)
    start_dt = datetime.combine(start_date, datetime.min.time(), tzinfo=timezone.utc)
    end_dt = datetime.combine(today_utc, datetime.min.time(), tzinfo=timezone.utc)
    start_ts, end_ts = int(start_dt.timestamp()), int(end_dt.timestamp())

    # Slice to last year
    return {ts: cnt for ts, cnt in merged.items() if start_ts <= ts < end_ts}

def fill_daily_activity(daily_activity: dict) -> dict:
    """
    Ensures every day in the last year is present in daily_activity, even if 0.
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

    return filled

def calculate_color(submissions: int, max_submissions: int, min_submissions: int) -> str:
    """
    Calculates an ANSI color code for a day’s submission count relative to min/max in the data.
    """
    CUSTOM_GREENS = [
        ANSI_CODES["GREEN1"],
        ANSI_CODES["GREEN2"],
        ANSI_CODES["GREEN3"],
        ANSI_CODES["GREEN4"],
        ANSI_CODES["GREEN5"],
        ANSI_CODES["GREEN6"]
    ]
    if max_submissions == min_submissions:
        return CUSTOM_GREENS[-1]

    normalized = (submissions - min_submissions) / (max_submissions - min_submissions)
    normalized = max(0.0, min(1.0, normalized))
    index = int(normalized * (len(CUSTOM_GREENS) - 1))
    return CUSTOM_GREENS[index]
