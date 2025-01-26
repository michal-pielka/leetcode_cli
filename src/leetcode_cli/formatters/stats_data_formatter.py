import logging
import re
import calendar
from datetime import datetime, timezone
from typing import Dict, List
from leetcode_cli.models.stats import UserStatsModel, UserActivityModel
from leetcode_cli.managers.theme_manager import ThemeManager
from leetcode_cli.exceptions.exceptions import ThemeError

logger = logging.getLogger(__name__)
DIFFICULTIES = ["EASY", "MEDIUM", "HARD"]


class StatsFormatter:
    """
    1) Difficulty-based stats (accepted, failed, untouched) with theming.
    2) Month-by-month heatmap calendar (8 rows x #weeks columns) horizontally joined.
    """

    ANSI_RESET = "\033[0m"
    CALENDAR_SHADE_STEPS = 8
    DAY_ABBREVIATIONS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    def __init__(self, theme_manager: ThemeManager):
        self.theme_manager = theme_manager
        self.theme_data = self.theme_manager.load_theme_data()

    def format_user_stats(self, stats: UserStatsModel) -> str:
        """
        Show difficulty-based stats, using "STATS" => difficulty_easy / medium / hard, etc.
        """
        lines = []

        for diff in DIFFICULTIES:
            accepted = stats.accepted.get(diff, 0)
            failed = stats.failed.get(diff, 0)
            untouched = stats.untouched.get(diff, 0)
            total_for_diff = accepted + failed + untouched
            beats_percentage = stats.beats.get(diff, 0.0)

            style_key = ""
            try:
                style_key = f"difficulty_{diff.lower()}"
                diff_ansi, diff_prefix, diff_suffix = self.theme_manager.get_styling(
                    "STATS_FORMATTER", style_key
                )

                style_key = f"correct_problems_{diff.lower()}"
                correct_ansi, correct_prefix, correct_suffix = (
                    self.theme_manager.get_styling("STATS_FORMATTER", style_key)
                )

                style_key = f"total_problems_{diff.lower()}"
                total_ansi, total_prefix, total_suffix = self.theme_manager.get_styling(
                    "STATS_FORMATTER", style_key
                )

                style_key = f"beats_number_{diff.lower()}"
                beats_number_ansi, beats_number_prefix, beats_number_suffix = (
                    self.theme_manager.get_styling("STATS_FORMATTER", style_key)
                )
            except ThemeError as te:
                logger.warning(f"Theme for {style_key} is missing: {te}")
                raise te

            line = f"{diff_ansi}{diff_prefix}{diff.ljust(8)}{diff_suffix}{self.ANSI_RESET} "
            line += f"{correct_ansi}{correct_prefix}{str(accepted).rjust(4)}{correct_suffix}{self.ANSI_RESET}"
            line += f"{total_ansi}{total_prefix}{str(total_for_diff).ljust(4)}{total_suffix}{self.ANSI_RESET}"
            line += f"{beats_number_ansi.ljust(4)}{str(beats_number_prefix)}{beats_percentage:.2f}{beats_number_suffix}"

            lines.append(line)

        return "\n".join(lines)

    def format_user_activity(self, activity: UserActivityModel) -> str:
        """
        Creates a horizontal layout of months, each an 8-row sub-grid:
          - row 0 => short month label
          - rows 1..7 => squares for Monday..Sunday
        Then merges the sub-grids horizontally with day labels on the left.
        """
        daily_activity = activity.daily_activity
        if not daily_activity:
            return "No activity data."

        # Convert {timestamp->count} => {date->count}
        date_counts: Dict[datetime.date, int] = {}
        for ts, count in daily_activity.items():
            try:
                dt = datetime.fromtimestamp(int(ts), tz=timezone.utc).date()
                date_counts[dt] = count
            except (ValueError, OverflowError) as e:
                raise e

        if not date_counts:
            return "No valid daily activity data."

        # If all zero, produce a simple message
        all_counts = list(date_counts.values())
        if max(all_counts) == 0:
            min_d = min(date_counts.keys())
            max_d = max(date_counts.keys())
            return f"All days from {min_d} to {max_d} have 0 submissions."

        lines = []

        try:
            least_ansi, least_prefix, least_suffix = self.theme_manager.get_styling(
                "STATS_FORMATTER", "calendar_least_submissions"
            )
        except ThemeError as te:
            raise te

        try:
            most_ansi, _, _ = self.theme_manager.get_styling(
                "STATS_FORMATTER", "calendar_most_submissions"
            )
        except ThemeError as te:
            raise te

        day_prefix = least_prefix
        day_suffix = least_suffix

        # 2) Build a color gradient based on the two "style" definitions
        gradient = self._build_color_gradient(least_ansi, most_ansi)

        min_sub = min(all_counts)
        max_sub = max(all_counts)

        # Identify earliest & latest month in the data
        min_date = min(date_counts.keys())
        max_date = max(date_counts.keys())

        subgrids = []
        year, month = min_date.year, min_date.month

        while True:
            # Build sub-grid for that month
            grid = self._build_month_subgrid(
                year,
                month,
                date_counts,
                gradient,
                day_prefix,
                day_suffix,
                min_sub,
                max_sub,
            )
            subgrids.append(grid)

            # If this is the last month, break
            if (year, month) == (max_date.year, max_date.month):
                break

            # Move to next month
            next_year, next_month = (year, month + 1) if month < 12 else (year + 1, 1)
            if (next_year, next_month) > (max_date.year, max_date.month):
                break
            year, month = next_year, next_month

        # Merge sub-grids horizontally => each sub-grid is 8 rows
        final_rows = []
        max_rows = 8
        for row_i in range(max_rows):
            row_parts = []
            for sg in subgrids:
                row_str = "".join(sg[row_i]) if row_i < len(sg) else ""
                row_parts.append(row_str)
            combined = (" " * 3).join(row_parts)
            if row_i == 0:
                # Prepend 4 spaces to align month row with day rows
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

    def _build_color_gradient(self, ansi_min, ansi_max) -> List[str]:
        """
        Build a color gradient using:
          - 'calendar_least_submissions' => e.g. style = "dark_green"
          - 'calendar_most_submissions' => e.g. style = "bright_green"
          - 'calendar_shade_steps' => e.g. 5
        We parse the min & max ANSI colors from the theme, extract (R,G,B),
        then interpolate for N=CALENDAR_SHADE_STEPS steps.
        """
        min_rgb = self._extract_rgb(ansi_min)
        max_rgb = self._extract_rgb(ansi_max)

        if not min_rgb or not max_rgb:
            logger.warning("Could not parse min/max ANSI color codes for the calendar.")
            return [""]

        (r1, g1, b1) = min_rgb
        (r2, g2, b2) = max_rgb

        gradient = []
        for i in range(self.CALENDAR_SHADE_STEPS):
            fraction = (
                (i / (self.CALENDAR_SHADE_STEPS - 1))
                if self.CALENDAR_SHADE_STEPS > 1
                else 0.0
            )
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

    def _get_gradient_color(
        self, c: int, min_c: int, max_c: int, gradient: List[str]
    ) -> str:
        """
        Map submission count c => an ANSI color from our gradient array.
        """
        if min_c == max_c:
            return gradient[-1]  # all the same color if min==max
        fraction = (c - min_c) / float(max_c - min_c)
        idx = int(round(fraction * (len(gradient) - 1)))
        return gradient[idx]

    def _build_month_subgrid(
        self,
        year: int,
        month: int,
        date_counts: Dict[datetime.date, int],
        gradient: List[str],
        day_prefix: str,
        day_suffix: str,
        min_sub: int,
        max_sub: int,
    ) -> List[List[str]]:
        """
        Return an 8-row 2D array for a single month:
          - row0 => short month label (e.g. "Jan")
          - row1..7 => squares for Mon..Sun
        """
        weeks = calendar.monthcalendar(year, month)
        height = 8  # row0 => label, row1..7 => squares
        width = len(weeks)
        subgrid = [[" " for _ in range(width)] for _ in range(height)]

        # Put short month name in row0
        short_label = calendar.month_abbr[month]  # e.g. "Jan"
        label_chars = list(short_label)
        for i, ch in enumerate(label_chars):
            if i < width:
                subgrid[0][i + 1] = ch

        # Fill squares for row=1..7, col=0..width-1
        # weeks[w][d] => day-of-month or 0, d=0..6 => Mon..Sun

        for col in range(width):
            wdays = weeks[col]  # [mon, tue, wed, thu, fri, sat, sun]
            for dow in range(7):
                day_num = wdays[dow]
                row = dow + 1  # row1 => Monday, row7 => Sunday
                if day_num == 0:
                    continue  # blank => out of month

                dt = datetime(year, month, day_num).date()
                c = date_counts.get(dt, 0)

                # Get the interpolated color from gradient
                day_ansi = self._get_gradient_color(c, min_sub, max_sub, gradient)

                day_str = f"{day_ansi}{day_prefix}{day_suffix}{self.ANSI_RESET}"

                subgrid[row][col] = day_str

        return subgrid
