# TODO: Tf is this code nigga

from datetime import datetime, timedelta, timezone
import sys
import calendar

# Import fetch functions (ensure these paths are correct in your project structure)
from ..data_fetching.graphql_data_fetchers.leetcode_stats import (
    fetch_leetcode_stats,
    fetch_leetcode_activity,
)

from ..graphics.symbols import SYMBOLS
from ..graphics.colors import COLORS

from ..parsers.parser_utils.leetcode_stats_parser import (
    join_and_slice_calendars,
    fill_daily_activity,
    calculate_color,
)

# Constants
RECTANGLES_TOTAL = 67
DIFFICULTIES = ["EASY", "MEDIUM", "HARD"]

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MONTH_SEPARATION = 3
COLUMNS = 100

def parse_leetcode_stats(data, username):
    """
    Parses LeetCode statistics and returns a formatted string.
    """
    try:
        user_progress = data["data"]["userProfileUserQuestionProgressV2"]

        # Extract counts by difficulty
        accepted = {item["difficulty"]: item["count"] for item in user_progress.get("numAcceptedQuestions", [])}
        failed = {item["difficulty"]: item["count"] for item in user_progress.get("numFailedQuestions", [])}
        untouched = {item["difficulty"]: item["count"] for item in user_progress.get("numUntouchedQuestions", [])}
        beats_percentage = {item["difficulty"]: item["percentage"] for item in user_progress.get("userSessionBeatsPercentage", [])}

        # Define colors for difficulties
        difficulty_colors = {
            "EASY": COLORS["GREEN"],
            "MEDIUM": COLORS["ORANGE"],
            "HARD": COLORS["RED"]
        }

        # Calculate total questions per difficulty
        total_questions = {}
        for difficulty in DIFFICULTIES:
            total = accepted.get(difficulty, 0) + failed.get(difficulty, 0) + untouched.get(difficulty, 0)
            total_questions[difficulty] = total

        stats_lines = []
        for difficulty in DIFFICULTIES:
            passed = accepted.get(difficulty, 0)
            total = total_questions[difficulty]
            percentage = beats_percentage.get(difficulty, 0.0)

            # Calculate filled rectangles
            if total > 0:
                filled = round((passed / total) * RECTANGLES_TOTAL)
            else:
                filled = 0
            filled = max(0, min(filled, RECTANGLES_TOTAL))  # Clamp between 0 and RECTANGLES_TOTAL
            progress_bar = SYMBOLS["FILLED_SQUARE"] * filled + SYMBOLS["EMPTY_SQUARE"] * (RECTANGLES_TOTAL - filled)

            # Formatting
            color = difficulty_colors.get(difficulty, COLORS["RESET_COLOR"])
            stats_line = (
                f"{color}{difficulty:<6} {passed:>4}/{total:<4} ({percentage:.2f}%) {progress_bar} {COLORS['RESET_COLOR']}"
            )
            stats_lines.append(stats_line)

        # Combine all outputs
        formatted_stats = f"LeetCode Stats for {username}\n" + "\n".join(stats_lines)
        return formatted_stats

    except (KeyError, TypeError, ZeroDivisionError) as error:
        print(f"Error parsing LeetCode stats: {error}", file=sys.stderr)
        return ""

def parse_daily_activity(filled_activity):
    """
    Parses daily activity and returns a formatted calendar string.
    """
    if not filled_activity:
        print("No daily activity data available", file=sys.stderr)
        return ""

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
        print("No valid daily activity data available", file=sys.stderr)
        return ""

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
            output[weekday][week_index] = f"{color}{SYMBOLS['FILLED_SQUARE']}{COLORS['RESET_COLOR']}"
        else:
            output[weekday][week_index] = f"{COLORS['GRAY']}{SYMBOLS['FILLED_SQUARE']}{COLORS['RESET_COLOR']}"

        # Check if it's the last day of the month
        last_day = calendar.monthrange(date.year, date.month)[1]
        if date.day == last_day and week_index < COLUMNS - 1:
            months_starting_indexes.append(week_index)
            week_index += MONTH_SEPARATION

        # Move to next day
        if weekday == 6:
            weekday = 0
            week_index += 1
        else:
            weekday += 1

    # Generate month labels
    MONTHS = [MONTH_NAMES[(min_date.month - 1 + i) % len(MONTH_NAMES)] for i in range(len(MONTH_NAMES))]
    months_parsed_list = [' ' for _ in range(COLUMNS)]

    for idx, start_index in enumerate(months_starting_indexes):
        month = MONTHS[(min_date.month + idx + 1) % 12]
        for i, char in enumerate(month):
            target_index = start_index - 3 + i
            if 0 <= target_index < COLUMNS:
                months_parsed_list[target_index] = char

    months_parsed = ''.join(months_parsed_list)

    # Generate calendar lines
    calendar_parsed = '\n'.join(''.join(row) for row in output)

    return f"{months_parsed}\n{calendar_parsed}"

def main():
    """
    Main function to fetch and display LeetCode stats and activity.
    """
    username = "BucketAbuser"

    # Fetch and parse stats
    stats = fetch_leetcode_stats(username)
    if stats:
        parsed_stats = parse_leetcode_stats(stats, username)
        print()
        print(parsed_stats)
    else:
        print("Failed to fetch LeetCode stats.", file=sys.stderr)

    # Fetch and parse activity
    current_year = datetime.now().year
    activity_past_year = fetch_leetcode_activity(username, current_year - 1)
    activity_this_year = fetch_leetcode_activity(username, current_year)
    sliced_activity = join_and_slice_calendars(activity_this_year, activity_past_year)
    filled_activity = fill_daily_activity(sliced_activity)

    if filled_activity:
        print()
        print()
        parsed_activity = parse_daily_activity(filled_activity)
        print(parsed_activity)
    else:
        print("Failed to fetch daily activity.", file=sys.stderr)

    print()
    print()


if __name__ == "__main__":
    main()
