import calendar
import logging
import re
from datetime import UTC, datetime

from leetcode_cli.managers.theme_manager import ThemeManager
from leetcode_cli.models.stats import UserActivityModel, UserStatsModel

logger = logging.getLogger(__name__)
DIFFICULTIES = ["EASY", "MEDIUM", "HARD"]


class StatsFormatter:
    """
    1) Difficulty-based stats (accepted, failed, untouched) with theming.
    2) Month-by-month heatmap calendar (8 rows x #weeks columns) horizontally joined.
    """

    CALENDAR_SHADE_STEPS = 8
    DAY_ABBREVIATIONS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    def __init__(self, theme_manager: ThemeManager):
        self.theme_manager = theme_manager
        self.theme_data = self.theme_manager.load_theme_data()
        self.ANSI_RESET = "" if theme_manager.raw_style else "\033[0m"

    def format_user_stats(self, stats: UserStatsModel) -> str:
        lines = []

        for diff in DIFFICULTIES:
            accepted = stats.accepted.get(diff, 0)
            failed = stats.failed.get(diff, 0)
            untouched = stats.untouched.get(diff, 0)
            total_for_diff = accepted + failed + untouched
            beats_percentage = stats.beats.get(diff, 0.0)

            diff_ansi, _ = self.theme_manager.get_styling("difficulty", diff.lower())

            line = f"{diff_ansi}{diff.ljust(8)}{self.ANSI_RESET} "
            line += f"{str(accepted).rjust(4)} /"
            line += f" {str(total_for_diff).ljust(4)}"
            line += f"({beats_percentage:.2f}%)"

            lines.append(line)

        return "\n".join(lines)

    def format_user_activity(self, activity: UserActivityModel) -> str:
        daily_activity = activity.daily_activity
        if not daily_activity:
            return "No activity data."

        date_counts: dict[datetime.date, int] = {}
        for ts, count in daily_activity.items():
            try:
                dt = datetime.fromtimestamp(int(ts), tz=UTC).date()
                date_counts[dt] = count
            except (ValueError, OverflowError) as e:
                raise e

        if not date_counts:
            return "No valid daily activity data."

        all_counts = list(date_counts.values())
        if max(all_counts) == 0:
            min_d = min(date_counts.keys())
            max_d = max(date_counts.keys())
            return f"All days from {min_d} to {max_d} have 0 submissions."

        lines = []

        least_ansi, day_icon = self.theme_manager.get_styling("calendar", "least_submissions")
        most_ansi, _ = self.theme_manager.get_styling("calendar", "most_submissions")

        gradient = self._build_color_gradient(least_ansi, most_ansi)

        min_sub = min(all_counts)
        max_sub = max(all_counts)

        min_date = min(date_counts.keys())
        max_date = max(date_counts.keys())

        subgrids = []
        year, month = min_date.year, min_date.month

        while True:
            grid = self._build_month_subgrid(
                year,
                month,
                date_counts,
                gradient,
                day_icon,
                min_sub,
                max_sub,
            )
            subgrids.append(grid)

            if (year, month) == (max_date.year, max_date.month):
                break

            next_year, next_month = (year, month + 1) if month < 12 else (year + 1, 1)
            if (next_year, next_month) > (max_date.year, max_date.month):
                break
            year, month = next_year, next_month

        final_rows = []
        max_rows = 8
        for row_i in range(max_rows):
            row_parts = []
            for sg in subgrids:
                row_str = "".join(sg[row_i]) if row_i < len(sg) else ""
                row_parts.append(row_str)
            combined = (" " * 3).join(row_parts)
            if row_i == 0:
                combined = "    " + combined
            elif 1 <= row_i <= 7:
                day_abbr = self.DAY_ABBREVIATIONS[row_i - 1]
                combined = f"{day_abbr}  {combined}"
            final_rows.append(combined)

        lines.extend(final_rows)
        return "\n".join(lines)

    #
    # ──────────────────────────────────────────────────────
    #   PRIVATE METHODS
    # ──────────────────────────────────────────────────────
    #

    def _build_color_gradient(self, ansi_min, ansi_max) -> list[str]:
        min_rgb = self._extract_rgb(ansi_min)
        max_rgb = self._extract_rgb(ansi_max)

        if not min_rgb or not max_rgb:
            logger.warning("Could not parse min/max ANSI color codes for the calendar.")
            return [""]

        (r1, g1, b1) = min_rgb
        (r2, g2, b2) = max_rgb

        gradient = []
        for i in range(self.CALENDAR_SHADE_STEPS):
            fraction = (i / (self.CALENDAR_SHADE_STEPS - 1)) if self.CALENDAR_SHADE_STEPS > 1 else 0.0
            rr = int(r1 + (r2 - r1) * fraction)
            gg = int(g1 + (g2 - g1) * fraction)
            bb = int(b1 + (b2 - b1) * fraction)
            gradient.append(f"\u001b[38;2;{rr};{gg};{bb}m")

        return gradient

    def _extract_rgb(self, ansi_code: str):
        """Parse something like '\\u001b[38;2;0;90;0m' => (0,90,0)."""
        match = re.search(r"38;2;(\d+);(\d+);(\d+)m", ansi_code)
        if match:
            return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
        return None

    def _get_gradient_color(self, c: int, min_c: int, max_c: int, gradient: list[str]) -> str:
        if min_c == max_c:
            return gradient[-1]
        fraction = (c - min_c) / float(max_c - min_c)
        idx = int(round(fraction * (len(gradient) - 1)))
        return gradient[idx]

    def _build_month_subgrid(
        self,
        year: int,
        month: int,
        date_counts: dict[datetime.date, int],
        gradient: list[str],
        day_icon: str,
        min_sub: int,
        max_sub: int,
    ) -> list[list[str]]:
        weeks = calendar.monthcalendar(year, month)
        height = 8
        width = len(weeks)
        subgrid = [[" " for _ in range(width)] for _ in range(height)]

        short_label = calendar.month_abbr[month]
        label_chars = list(short_label)
        for i, ch in enumerate(label_chars):
            if i + 1 < width:
                subgrid[0][i + 1] = ch

        for col in range(width):
            wdays = weeks[col]
            for dow in range(7):
                day_num = wdays[dow]
                row = dow + 1
                if day_num == 0:
                    continue

                dt = datetime(year, month, day_num).date()
                c = date_counts.get(dt, 0)

                day_ansi = self._get_gradient_color(c, min_sub, max_sub, gradient)
                day_str = f"{day_ansi}{day_icon}{self.ANSI_RESET}"

                subgrid[row][col] = day_str

        return subgrid
