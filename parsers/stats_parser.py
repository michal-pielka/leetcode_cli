from datetime import datetime, timedelta, timezone
import logging

from ..graphics.symbols import SYMBOLS
from ..graphics.escape_sequences import ANSI_CODES, ANSI_RESET
from .parser_utils.stats_parser_utils import (
    join_and_slice_calendars,
    fill_daily_activity,
    calculate_color,
)

logger = logging.getLogger(__name__)

class LeetCodeStatsParserError(Exception):
    """Custom exception for LeetCodeStatsParser errors."""
    pass

RECTANGLES_TOTAL = 66
DIFFICULTIES = ["EASY", "MEDIUM", "HARD"]
MONTH_NAMES = [
    "Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]
MONTH_SEPARATION = 3
COLUMNS = 100

def get_formatted_leetcode_stats(data: dict) -> str:
    try:
        user_progress = data["data"]["userProfileUserQuestionProgressV2"]

        # Extract counts by difficulty
        accepted = {item["difficulty"].upper(): item["count"] for item in user_progress.get("numAcceptedQuestions", [])}
        failed = {item["difficulty"].upper(): item["count"] for item in user_progress.get("numFailedQuestions", [])}
        untouched = {item["difficulty"].upper(): item["count"] for item in user_progress.get("numUntouchedQuestions", [])}
        logger.debug(f"Accepted: {accepted}, Failed: {failed}, Untouched: {untouched}")

        # Calculate total per difficulty
        total_counts = {}
        for difficulty in DIFFICULTIES:
            total_counts[difficulty] = (
                accepted.get(difficulty, 0) +
                failed.get(difficulty, 0) +
                untouched.get(difficulty, 0)
            )

        # Define colors for difficulties
        difficulty_colors = {
            "EASY": ANSI_CODES["GREEN"],
            "MEDIUM": ANSI_CODES["ORANGE"],
            "HARD": ANSI_CODES["RED"]
        }

        stats_lines = []
        for difficulty in DIFFICULTIES:
            passed = accepted.get(difficulty, 0)
            total = total_counts.get(difficulty, 0)

            if total == 0:
                percentage = 0.0
            else:
                percentage = (passed / total) * 100

            # Calculate filled rectangles
            progress_ratio = passed / total if total > 0 else 0.0
            filled = int(round(progress_ratio * RECTANGLES_TOTAL))
            filled = max(0, min(filled, RECTANGLES_TOTAL))  # Clamp between 0 and RECTANGLES_TOTAL

            # Create progress bar
            filled_bar = SYMBOLS['FILLED_SQUARE'] * filled
            empty_bar = SYMBOLS['EMPTY_SQUARE'] * (RECTANGLES_TOTAL - filled)
            progress_bar = filled_bar + empty_bar

            # Get the color for the entire line
            color = difficulty_colors.get(difficulty, ANSI_RESET)

            # Formatting
            stats_line = (
                f"{color}{difficulty:<7} {passed:>4}/{total:<4} ({percentage:.2f}%) {progress_bar}{ANSI_RESET}"
            )
            stats_lines.append(stats_line)

        # Combine all outputs
        formatted_stats = "\n".join(stats_lines)
        return formatted_stats

    except (KeyError, TypeError, ZeroDivisionError) as error:
        logger.error(f"Error parsing LeetCode stats: {error}")
        raise LeetCodeStatsParserError(f"Error parsing LeetCode stats: {error}")

def get_formatted_daily_activity(filled_activity: dict) -> str:
    """
    Parses daily activity and returns a formatted calendar string.

    Args:
        filled_activity (dict): A dictionary with timestamps as keys and submission counts as values.

    Returns:
        str: A formatted string representing the activity calendar.

    Raises:
        LeetCodeStatsParserError: If activity data is invalid.
    """
    if not filled_activity:
        logger.error("No daily activity data available")
        raise LeetCodeStatsParserError("No daily activity data available")

    # Initialize output: 7 rows for days of the week, COLUMNS weeks
    output = [[' ' for _ in range(COLUMNS)] for _ in range(7)]

    # Convert timestamps to dates and map counts
    date_counts = {}
    for ts, count in filled_activity.items():
        try:
            date = datetime.fromtimestamp(int(ts), tz=timezone.utc).date()
            date_counts[date] = count
        except (ValueError, OverflowError):
            continue  # Skip invalid timestamps

    if not date_counts:
        logger.error("No valid daily activity data available")
        raise LeetCodeStatsParserError("No valid daily activity data available")

    months_starting_indexes = []

    # Determine the date range
    min_date = min(date_counts.keys())
    max_date = max(date_counts.keys())
    min_submissions = min(date_counts.values())
    max_submissions = max(date_counts.values())

    # Generate all dates from start_date to end_date
    total_days = (max_date - min_date).days + 1
    all_dates = [min_date + timedelta(days=i) for i in range(total_days)]

    # Initialize tracking variables
    weekday = all_dates[0].weekday()  # Monday=0, Sunday=6
    week_index = 3  # Starting week index
    for date in all_dates:
        submissions = date_counts.get(date, 0)

        if submissions > 0:
            color = calculate_color(submissions, max_submissions, min_submissions)
            output[weekday][week_index] = f"{color}{SYMBOLS['FILLED_SQUARE']}{ANSI_RESET}"
        else:
            output[weekday][week_index] = f"{ANSI_CODES['GRAY']}{SYMBOLS['FILLED_SQUARE']}{ANSI_RESET}"

        # Check if it's the last day of the month
        if date.day == 1 and week_index < COLUMNS - 1:
            months_starting_indexes.append(week_index)
            week_index += MONTH_SEPARATION

        # Move to next day
        if weekday == 6:
            weekday = 0
            week_index += 1
        else:
            weekday += 1

    # Generate month labels
    months_parsed_list = [' ' for _ in range(COLUMNS)]
    for idx, start_index in enumerate(months_starting_indexes):
        month = MONTH_NAMES[(min_date.month + idx - 1) % 12]
        for i, char in enumerate(month):
            target_index = start_index - 3 + i
            if 0 <= target_index < COLUMNS:
                months_parsed_list[target_index] = char

    months_parsed = ''.join(months_parsed_list)

    # Generate calendar lines
    calendar_parsed = '\n'.join(''.join(row) for row in output)

    return f"{months_parsed}\n{calendar_parsed}"
