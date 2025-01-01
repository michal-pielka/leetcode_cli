from datetime import datetime, timedelta, timezone
import logging

from leetcode_cli.models.stats import UserStatsModel, UserActivityModel
from leetcode_cli.models.theme import ThemeData
from leetcode_cli.constants.stats_constants import RECTANGLES_TOTAL, MONTH_SEPARATION, DIFFICULTIES, COLUMNS, MONTH_NAMES
from leetcode_cli.graphics.ansi_codes import ANSI_RESET
from leetcode_cli.services.stats_service import calculate_color
from leetcode_cli.services.theme_service import get_ansi_code, get_symbol

logger = logging.getLogger(__name__)

class StatsFormatter:
    def __init__(self, theme_data: ThemeData):
        self.theme_data = theme_data

    def format_user_stats(self, stats: UserStatsModel) -> str:
        lines = []
        for difficulty in DIFFICULTIES:
            passed = stats.accepted.get(difficulty, 0)
            failed = stats.failed.get(difficulty, 0)
            untouched = stats.untouched.get(difficulty, 0)
            total = passed + failed + untouched
            percentage = (passed / total * 100) if total else 0.0

            progress_ratio = (passed / total) if total else 0.0
            filled = int(round(progress_ratio * RECTANGLES_TOTAL))
            filled = max(0, min(filled, RECTANGLES_TOTAL))

            # --------------- REMOVE fallback logic; just let ThemeError bubble up ---------------
            filled_square = get_symbol(self.theme_data, 'STATS_FORMATTER_SYMBOLS', 'FILLED_SQUARE')
            empty_square = get_symbol(self.theme_data, 'STATS_FORMATTER_SYMBOLS', 'EMPTY_SQUARE')
            # ------------------------------------------------------------------------------------

            filled_bar = filled_square * filled
            empty_bar = empty_square * (RECTANGLES_TOTAL - filled)
            progress_bar = filled_bar + empty_bar

            # --------------- REMOVE fallback logic; just let ThemeError bubble up ---------------
            color = get_ansi_code(self.theme_data, 'STATS_FORMATTER_DIFFICULTY_COLORS', difficulty)
            # ------------------------------------------------------------------------------------

            line = f"{color}{difficulty:<7} {passed:>4}/{total:<4} ({percentage:.2f}%) {progress_bar}{ANSI_RESET}"
            lines.append(line)

        return "\n".join(lines)

    def format_user_activity(self, activity: UserActivityModel) -> str:
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
                # --------------- REMOVE fallback logic; just let ThemeError bubble up ---------------
                filled_square = get_symbol(self.theme_data, 'STATS_FORMATTER_SYMBOLS', 'FILLED_SQUARE')
                # ------------------------------------------------------------------------------------
                output[weekday][week_index] = f"{color}{filled_square}{ANSI_RESET}"
            else:
                # --------------- REMOVE fallback logic; just let ThemeError bubble up ---------------
                gray_color = get_ansi_code(self.theme_data, 'STATS_FORMATTER_DIFFICULTY_COLORS', 'CALENDAR_TIER0')
                filled_square = get_symbol(self.theme_data, 'STATS_FORMATTER_SYMBOLS', 'FILLED_SQUARE')
                # ------------------------------------------------------------------------------------
                output[weekday][week_index] = f"{gray_color}{filled_square}{ANSI_RESET}"

            if date.day == 1 and week_index < COLUMNS - 1:
                week_index += MONTH_SEPARATION
            if weekday == 6:
                weekday = 0
                week_index += 1
            else:
                weekday += 1

        # Mark months
        output_months = [' ' for _ in range(COLUMNS)]
        months_starting_indexes = []
        week_index = 3
        weekday = all_dates[0].weekday()

        for date in all_dates:
            if date.day == 1 and week_index < COLUMNS - 1:
                months_starting_indexes.append(week_index)
            if weekday == 6:
                weekday = 0
                week_index += 1
            else:
                weekday += 1

        for idx, start_index in enumerate(months_starting_indexes):
            month = MONTH_NAMES[(min_date.month + idx - 1) % 12]
            for i, char in enumerate(month):
                target_index = start_index - 3 + i
                if 0 <= target_index < COLUMNS:
                    output_months[target_index] = char

        months_parsed = ''.join(output_months)
        calendar_parsed = '\n'.join(''.join(row) for row in output)

        return f"{months_parsed}\n{calendar_parsed}"
