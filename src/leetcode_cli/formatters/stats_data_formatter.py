import logging
from datetime import datetime, timedelta, timezone
from leetcode_cli.models.stats import UserStatsModel, UserActivityModel
from leetcode_cli.models.theme import ThemeData
from leetcode_cli.graphics.ansi_codes import ANSI_RESET
from leetcode_cli.constants.stats_constants import (
    RECTANGLES_TOTAL, MONTH_SEPARATION, DIFFICULTIES, COLUMNS, MONTH_NAMES
)
from leetcode_cli.services.stats_service import calculate_color
from leetcode_cli.services.theme_service import get_styling
from leetcode_cli.exceptions.exceptions import ThemeError

logger = logging.getLogger(__name__)

class StatsFormatter:
    """
    Formats user stats (counts per difficulty) and activity calendar.
    """
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

            ratio = (passed / total) if total else 0.0
            filled = int(round(ratio * RECTANGLES_TOTAL))

            try:
                # Get symbols
                filled_ansi, filled_symbol_left, filled_symbol_right = get_styling(self.theme_data, 'STATS_FORMATTER', 'filled_square')
                empty_ansi, empty_symbol_left, empty_symbol_right = get_styling(self.theme_data, 'STATS_FORMATTER', 'empty_square')

                # ANSI color for the difficulty
                diff_ansi, diff_symbol_left, diff_symbol_right = get_styling(self.theme_data, 'STATS_FORMATTER', difficulty.upper())

                # Build the bar with each symbol wrapped
                filled_bar = ''.join([f"{diff_ansi}{filled_symbol_left}{filled_symbol_right}{ANSI_RESET}" for _ in range(filled)])
                empty_bar = ''.join([f"{diff_ansi}{empty_symbol_left}{empty_symbol_right}{ANSI_RESET}" for _ in range(RECTANGLES_TOTAL - filled)])
                bar = filled_bar + empty_bar

                # Combine all parts with proper styling
                line = f"{diff_ansi}{difficulty:<7}{diff_symbol_left}{diff_symbol_right}{ANSI_RESET} {passed:>4}/{total:<4} ({percentage:.2f}%) {bar}"
                lines.append(line)
            except ThemeError as te:
                logger.error(f"Theming Error in format_user_stats: {te}")
                raise te

        return "\n".join(lines)

    def format_user_activity(self, activity: UserActivityModel) -> str:
        daily_activity = activity.daily_activity
        if not daily_activity:
            return "No activity data."

        output = [[' ' for _ in range(COLUMNS)] for _ in range(7)]
        date_counts = {}
        for ts, count in daily_activity.items():
            try:
                dt = datetime.fromtimestamp(int(ts), tz=timezone.utc).date()
                date_counts[dt] = count
            except (ValueError, OverflowError):
                continue

        if not date_counts:
            return "No valid daily activity data."

        min_date = min(date_counts.keys())
        max_date = max(date_counts.keys())

        min_sub = min(date_counts.values())
        max_sub = max(date_counts.values())

        total_days = (max_date - min_date).days + 1
        all_dates = [min_date + timedelta(days=i) for i in range(total_days)]

        weekday = all_dates[0].weekday()
        week_index = 3

        for date in all_dates:
            subs = date_counts.get(date, 0)
            if subs > 0:
                try:
                    # Determine tier based on submissions
                    if subs == 1:
                        tier = 'CALENDAR_TIER1'
                    else:
                        tier = 'CALENDAR_TIER1'  # You can define more tiers if needed
                    color, symbol_left, symbol_right = get_styling(self.theme_data, 'STATS_FORMATTER', tier)
                    symbol = get_styling(self.theme_data, 'STATS_FORMATTER', 'filled_square')[1]
                    output[weekday][week_index] = f"{color}{symbol_left}{symbol}{symbol_right}{ANSI_RESET}"
                except ThemeError as te:
                    logger.error(f"Theming Error in format_user_activity: {te}")
                    raise te
            else:
                try:
                    tier0_ansi, tier0_symbol_left, tier0_symbol_right = get_styling(self.theme_data, 'STATS_FORMATTER', 'CALENDAR_TIER0')
                    symbol = get_styling(self.theme_data, 'STATS_FORMATTER', 'empty_square')[1]
                    output[weekday][week_index] = f"{tier0_ansi}{tier0_symbol_left}{symbol}{tier0_symbol_right}{ANSI_RESET}"
                except ThemeError as te:
                    logger.error(f"Theming Error in format_user_activity: {te}")
                    raise te

            if date.day == 1 and week_index < COLUMNS - 1:
                week_index += MONTH_SEPARATION
            if weekday == 6:
                weekday = 0
                week_index += 1
            else:
                weekday += 1

        # Mark months
        output_months = [' ' for _ in range(COLUMNS)]
        months_starts = []
        week_index = 3
        weekday = all_dates[0].weekday()

        for date in all_dates:
            if date.day == 1 and week_index < COLUMNS - 1:
                months_starts.append(week_index)
            if weekday == 6:
                weekday = 0
                week_index += 1
            else:
                weekday += 1

        for idx, start_idx in enumerate(months_starts):
            month = MONTH_NAMES[(min_date.month + idx - 1) % 12]
            for i, char in enumerate(month):
                tgt = start_idx - 3 + i
                if 0 <= tgt < COLUMNS:
                    output_months[tgt] = char

        months_parsed = ''.join(output_months)
        cal_parsed = '\n'.join(''.join(row) for row in output)
        return f"{months_parsed}\n{cal_parsed}"
