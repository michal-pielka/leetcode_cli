# TODO: Fix deprecated values

import json
from datetime import datetime, timezone

from ...graphics.escape_sequences import ANSI_CODES


def join_and_slice_calendars(previous_year_calendar: dict, current_year_calendar: dict) -> dict:
    """
    Joins and slices the activity calendars from the previous and current years.

    Args:
        previous_year_calendar (dict): The calendar data for the previous year.
        current_year_calendar (dict): The calendar data for the current year.

    Returns:
        dict: A dictionary with timestamps as keys and submission counts as values.
    """
    if not previous_year_calendar or not current_year_calendar:
        return {}

    try:
        # Load activity data from JSON strings
        previous_activity = json.loads(
            previous_year_calendar['data']['matchedUser']['userCalendar']['submissionCalendar']
        )
        current_activity = json.loads(
            current_year_calendar['data']['matchedUser']['userCalendar']['submissionCalendar']
        )

    except KeyError as error:
        print(f"Missing key in submission_calendar data: {error}")
        return {}

    except json.JSONDecodeError as error:
        print(f"JSON decoding error: {error}")
        return {}

    # Merge activities ensuring the combined dictionary has all timestamps
    merged_activity = {**previous_activity, **current_activity}

    # Convert keys to integers
    merged_activity = {int(timestamp): count for timestamp, count in merged_activity.items()}

    # Get today's date in UTC
    today_utc = datetime.utcnow().date()

    # Handle the special case for leap years
    if today_utc.month == 2 and today_utc.day == 29:
        # Roll back to March 1 of the previous year
        start_date = today_utc.replace(year=today_utc.year - 1, month=3, day=1)
    else:
        start_date = today_utc.replace(year=today_utc.year - 1)

    # Create start and end datetime objects
    start_datetime = datetime(
        year=start_date.year,
        month=start_date.month,
        day=start_date.day,
        tzinfo=timezone.utc
    )

    end_datetime = datetime(
        year=today_utc.year,
        month=today_utc.month,
        day=today_utc.day,
        tzinfo=timezone.utc
    )

    start_timestamp = int(start_datetime.timestamp())
    end_timestamp = int(end_datetime.timestamp())

    sliced_activity = {timestamp: count for timestamp, count in merged_activity.items()
                       if start_timestamp <= timestamp < end_timestamp}

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

    # Handle the special case for leap years
    if today_utc.month == 2 and today_utc.day == 29:
        start_date = today_utc.replace(year=today_utc.year - 1, month=3, day=1)
    else:
        start_date = today_utc.replace(year=today_utc.year - 1)

    # Create start and end datetime objects
    start_datetime = datetime(
        year=start_date.year,
        month=start_date.month,
        day=start_date.day,
        tzinfo=timezone.utc
    )
    end_datetime = datetime(
        year=today_utc.year,
        month=today_utc.month,
        day=today_utc.day,
        tzinfo=timezone.utc
    )

    # Convert to timestamps
    start_timestamp = int(start_datetime.timestamp())
    end_timestamp = int(end_datetime.timestamp())

    # Generate all daily timestamps within the past year
    current_timestamp = start_timestamp

    while current_timestamp <= end_timestamp:
        filled_activity[current_timestamp] = daily_activity.get(current_timestamp, 0)
        current_timestamp += 86400  # Increment by one day (in seconds)

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
