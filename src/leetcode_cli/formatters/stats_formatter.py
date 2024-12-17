# leetcode_cli/formatters/stats_formatter.py
from leetcode_cli.models.stats import UserStatsModel, UserActivityModel
from leetcode_cli.utils.stats_utils import calculate_color
from leetcode_cli.constants.stats_constants import RECTANGLES_TOTAL, MONTH_SEPARATION, DIFFICULTIES, COLUMNS, MONTH_NAMES
from leetcode_cli.utils.theme_utils import get_theme_data, get_themes_dir
from leetcode_cli.graphics.ansi_codes import ANSI_RESET

from datetime import datetime, timedelta, timezone

import logging
logger = logging.getLogger(__name__)


THEME_DATA = get_theme_data()

def format_user_stats(stats: UserStatsModel) -> str:
    stats_lines = []
    for difficulty in DIFFICULTIES:
        passed = stats.accepted.get(difficulty, 0)
        total = (passed +
                 stats.failed.get(difficulty, 0) +
                 stats.untouched.get(difficulty, 0))
        if total == 0:
            percentage = 0.0
        else:
            percentage = (passed / total) * 100

        progress_ratio = passed / total if total > 0 else 0.0
        filled = int(round(progress_ratio * RECTANGLES_TOTAL))
        filled = max(0, min(filled, RECTANGLES_TOTAL))

        filled_bar = THEME_DATA['STATS_FORMATTER_SYMBOLS']['FILLED_SQUARE'] * filled
        empty_bar = THEME_DATA['STATS_FORMATTER_SYMBOLS']['EMPTY_SQUARE'] * (RECTANGLES_TOTAL - filled)
        progress_bar = filled_bar + empty_bar

        color = THEME_DATA['STATS_FORMATTER_DIFFICULTY_COLORS'].get(difficulty, ANSI_RESET)
        line = f"{color}{difficulty:<7} {passed:>4}/{total:<4} ({percentage:.2f}%) {progress_bar}{ANSI_RESET}"
        stats_lines.append(line)

    return "\n".join(stats_lines)

def format_user_activity(activity: UserActivityModel) -> str:
    daily_activity = activity.daily_activity
    if not daily_activity:
        return "No activity data."

    output = [[' ' for _ in range(COLUMNS)] for _ in range(7)]
    date_counts = {}
    for ts, count in daily_activity.items():
        try:
            date = datetime.fromtimestamp(int(ts), tz=timezone.utc).date()
            date_counts[date] = count
        except (ValueError, OverflowError):
            continue

    if not date_counts:
        return "No valid daily activity data."

    months_starting_indexes = []
    min_date = min(date_counts.keys())
    max_date = max(date_counts.keys())
    min_submissions = min(date_counts.values())
    max_submissions = max(date_counts.values())

    total_days = (max_date - min_date).days + 1
    all_dates = [min_date + timedelta(days=i) for i in range(total_days)]

    weekday = all_dates[0].weekday()
    week_index = 3
    for date in all_dates:
        submissions = date_counts.get(date, 0)
        if submissions > 0:
            color = calculate_color(submissions, max_submissions, min_submissions)
            output[weekday][week_index] = f"{color}{THEME_DATA['STATS_FORMATTER_SYMBOLS']['FILLED_SQUARE']}{ANSI_RESET}"
        else:
            # Use a gray fill for no submissions
            gray_color = THEME_DATA['STATS_FORMATTER_DIFFICULTY_COLORS'].get('CALENDAR_TIER0', ANSI_RESET)
            output[weekday][week_index] = f"{gray_color}{THEME_DATA['STATS_FORMATTER_SYMBOLS']['FILLED_SQUARE']}{ANSI_RESET}"

        if date.day == 1 and week_index < COLUMNS - 1:
            months_starting_indexes.append(week_index)
            week_index += MONTH_SEPARATION

        if weekday == 6:
            weekday = 0
            week_index += 1
        else:
            weekday += 1

    months_parsed_list = [' ' for _ in range(COLUMNS)]
    for idx, start_index in enumerate(months_starting_indexes):
        month = MONTH_NAMES[(min_date.month + idx - 1) % 12]
        for i, char in enumerate(month):
            target_index = start_index - 3 + i
            if 0 <= target_index < COLUMNS:
                months_parsed_list[target_index] = char

    months_parsed = ''.join(months_parsed_list)
    calendar_parsed = '\n'.join(''.join(row) for row in output)
    return f"{months_parsed}\n{calendar_parsed}"
