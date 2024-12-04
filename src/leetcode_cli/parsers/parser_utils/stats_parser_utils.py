import json
from datetime import datetime, timezone, timedelta
import logging

from ...graphics.escape_sequences import ANSI_CODES

logger = logging.getLogger(__name__)

def join_and_slice_calendars(previous_year_calendar: dict, current_year_calendar: dict) -> dict:
    """
    Joins and slices the activity calendars from the previous and current years.

    Args:
        previous_year_calendar (dict): The calendar data for the previous year.
        current_year_calendar (dict): The calendar data for the current year.

    Returns:
        dict: A dictionary with timestamps as keys and submission counts as values.

    Raises:
        Exception: If data is invalid or missing.
    """
    if not previous_year_calendar or not current_year_calendar:
        raise Exception("Previous or current year calendar data is missing.")

    try:
        # Load activity data from JSON strings
        previous_activity = json.loads(
            previous_year_calendar['data']['matchedUser']['userCalendar']['submissionCalendar']
        )
        current_activity = json.loads(
            current_year_calendar['data']['matchedUser']['userCalendar']['submissionCalendar']
        )

    except KeyError as error:
        logger.error(f"Missing key in submission_calendar data: {error}")
        raise Exception(f"Missing key in submission_calendar data: {error}")

    except json.JSONDecodeError as error:
        logger.error(f"JSON decoding error: {error}")
        raise Exception(f"JSON decoding error: {error}")

    # Merge activities ensuring the combined dictionary has all timestamps
    merged_activity = {**previous_activity, **current_activity}

    # Convert keys to integers
    merged_activity = {int(timestamp): count for timestamp, count in merged_activity.items()}

    # Get today's date in UTC
    today_utc = datetime.utcnow().date()
    start_date = today_utc - timedelta(days=365)

    # Create start and end datetime objects
    start_datetime = datetime.combine(start_date, datetime.min.time(), tzinfo=timezone.utc)
    end_datetime = datetime.combine(today_utc, datetime.min.time(), tzinfo=timezone.utc)

    start_timestamp = int(start_datetime.timestamp())
    end_timestamp = int(end_datetime.timestamp())

    sliced_activity = {
        timestamp: count for timestamp, count in merged_activity.items()
        if start_timestamp <= timestamp < end_timestamp
    }

    return sliced_activity

def fill_daily_activity(daily_activity: dict) -> dict:
    """
    Fills the daily activity dictionary to ensure every day in the past year is represented.

    Args:
        daily_activity (dict): The original activity data.

    Returns:
        dict: A filled dictionary with timestamps for each day.
    """
    filled_activity = {}
    today_utc = datetime.utcnow().date()
    start_date = today_utc - timedelta(days=365)

    # Create start and end datetime objects
    start_datetime = datetime.combine(start_date, datetime.min.time(), tzinfo=timezone.utc)
    end_datetime = datetime.combine(today_utc, datetime.min.time(), tzinfo=timezone.utc)

    # Generate all daily timestamps within the past year
    current_datetime = start_datetime

    while current_datetime <= end_datetime:
        timestamp = int(current_datetime.timestamp())
        filled_activity[timestamp] = daily_activity.get(timestamp, 0)
        current_datetime += timedelta(days=1)

    return filled_activity

def calculate_color(submissions: int, max_submissions: int, min_submissions: int) -> str:
    """
    Calculates the color code based on the number of submissions.

    Args:
        submissions (int): The number of submissions on a particular day.
        max_submissions (int): The maximum number of submissions in the dataset.
        min_submissions (int): The minimum number of submissions in the dataset.

    Returns:
        str: The ANSI color code.
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
        # Avoid division by zero; default to the brightest green
        return CUSTOM_GREENS[-1]

    # Normalize submissions to a value between 0 and 1
    normalized = (submissions - min_submissions) / (max_submissions - min_submissions)
    normalized = max(0.0, min(1.0, normalized))  # Clamp between 0 and 1

    # Determine the index in the CUSTOM_GREENS list
    index = int(normalized * (len(CUSTOM_GREENS) - 1))

    return CUSTOM_GREENS[index]
