# file: formatters/stats_data_formatter.py

import logging
import re
import calendar
from datetime import datetime, timezone
from typing import Dict, List
from leetcode_cli.models.stats import UserStatsModel, UserActivityModel
from leetcode_cli.constants.stats_constants import DIFFICULTIES
from leetcode_cli.managers.theme_manager import ThemeManager
from leetcode_cli.exceptions.exceptions import ThemeError

logger = logging.getLogger(__name__)


class StatsFormatter:
    """
    Formats:
      1) Per-difficulty stats (accepted, failed, untouched) with theming from "STATS".
      2) A horizontally oriented, month-by-month "heatmap"-style calendar,
         where each month is a sub-grid (8 rows x #weeks columns):
           - row=0 => short month label
           - row=1..7 => squares for Monday..Sunday
         We then horizontally join these sub-grids with 3 spaces in between.
    """

    ANSI_RESET = "\033[0m"
    CALENDAR_SHADE_STEPS = 8

    def __init__(self, theme_manager: ThemeManager):
        self.theme_manager = theme_manager
        # Load entire theme data (ANSI_CODES, STATS_FORMATTER, etc.)
        self.theme_data = self.theme_manager.load_theme_data()

    def format_user_stats(self, stats: UserStatsModel) -> str:
        """
        Show difficulty-based stats, using "STATS" => difficulty_easy / medium / hard, etc.
        """
        lines = []
        lines.append("=== USER STATS ===")

        for diff in DIFFICULTIES:
            accepted = stats.accepted.get(diff, 0)
            failed = stats.failed.get(diff, 0)
            untouched = stats.untouched.get(diff, 0)
            total_for_diff = accepted + failed + untouched
            beats_percentage = stats.beats.get(diff, 0.0)

            style_key = f"difficulty_{diff.lower()}"
            try:
                diff_ansi, diff_prefix, diff_suffix = self.theme_manager.get_styling(
                    "STATS", style_key
                )
            except ThemeError as te:
                logger.warning(f"Theme for {style_key} is missing: {te}")
                diff_ansi = diff_prefix = diff_suffix = ""

            line = (
                f"{diff_ansi}{diff_prefix}{diff.capitalize()}{diff_suffix}{self.ANSI_RESET}"
                f": Solved {accepted}/{total_for_diff} "
                f"(Beat: {beats_percentage:.2f}%)"
            )
            lines.append(line)

        lines.append(f"Total Submissions (approx): {stats.total_submissions}")
        return "\n".join(lines)

    def format_user_activity(self, activity: UserActivityModel) -> str:
        """
        Creates a horizontal layout of months, each an 8-row sub-grid:
          - row 0 => short month label
          - rows 1..7 => squares for Monday..Sunday

        Then merges these month sub-grids side-by-side with 3 spaces between them.
        Uses STATS_FORMATTER for:
          - calendar_symbol
          - calendar_least_submissions, calendar_most_submissions
          - calendar_shade_steps
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
            except (ValueError, OverflowError):
                continue

        if not date_counts:
            return "No valid daily activity data."

        # Check if all zero
        all_counts = list(date_counts.values())
        if max(all_counts) == 0:
            min_d = min(date_counts.keys())
            max_d = max(date_counts.keys())
            return (
                "=== ACTIVITY CALENDAR ===\n"
                f"All days from {min_d} to {max_d} have 0 submissions."
            )

        lines = ["=== ACTIVITY CALENDAR ==="]

        # Build gradient & fetch symbol
        gradient = self._build_color_gradient()
        symbol = self.theme_data.STATS_FORMATTER.get("calendar_symbol", "■")

        min_sub = min(all_counts)
        max_sub = max(all_counts)

        # Identify earliest & latest month in the data
        min_date = min(date_counts.keys())
        max_date = max(date_counts.keys())

        # We'll loop from (year= min_date.year, month= min_date.month)
        # up to (max_date.year, max_date.month).
        subgrids = []
        year, month = min_date.year, min_date.month

        while True:
            # Build sub-grid for that month
            grid = self._build_month_subgrid(
                year, month, date_counts, gradient, symbol, min_sub, max_sub
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
        # We'll create 8 final lines. For row i in 0..7, join subgrids[row i] with 3 spaces
        final_rows = []
        max_rows = 8
        for row_i in range(max_rows):
            row_parts = []
            for sg in subgrids:
                # each sg is an 8 x W 2D array => row_i => list of strings
                row_str = "".join(sg[row_i]) if row_i < len(sg) else ""
                row_parts.append(row_str)
            # Join sub-grids with 3 spaces
            combined = (" " * 3).join(row_parts)
            final_rows.append(combined)

        lines.extend(final_rows)
        return "\n".join(lines)

    #
    # ──────────────────────────────────────────────────────
    #   PRIVATE METHODS
    # ──────────────────────────────────────────────────────
    #

    def _build_color_gradient(self) -> List[str]:
        """
        Build gradient from STATS_FORMATTER keys:
          calendar_least_submissions => e.g. "dark_green"
          calendar_most_submissions => e.g. "bright_green"
          calendar_shade_steps => e.g. 5
        We parse from ANSI_CODES, extract (R,G,B), generate intermediate steps.
        """
        sf = self.theme_data.STATS_FORMATTER
        try:
            min_color_key = sf["calendar_least_submissions"]
            max_color_key = sf["calendar_most_submissions"]
        except KeyError as e:
            logger.warning(f"Missing key in STATS_FORMATTER: {e}")
            return [""]

        ansi_min = self.theme_data.ANSI_CODES.get(min_color_key, "")
        ansi_max = self.theme_data.ANSI_CODES.get(max_color_key, "")

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
        """
        Parse something like '\\u001b[38;2;0;90;0m' => (0,90,0).
        Return None if parse fails.
        """
        match = re.search(r"38;2;(\d+);(\d+);(\d+)m", ansi_code)
        if match:
            return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
        return None

    def _get_gradient_color(
        self, c: int, min_c: int, max_c: int, gradient: List[str]
    ) -> str:
        """
        Map submission count c => gradient index.
        """
        if min_c == max_c:
            return gradient[-1]  # all the same
        fraction = (c - min_c) / float(max_c - min_c)
        idx = int(round(fraction * (len(gradient) - 1)))
        return gradient[idx]

    def _build_month_subgrid(
        self,
        year: int,
        month: int,
        date_counts: Dict[datetime.date, int],
        gradient: List[str],
        symbol: str,
        min_sub: int,
        max_sub: int,
    ) -> List[List[str]]:
        """
        Return an 8-row 2D array representing a single month sub-grid:
          - row 0 => short month label (e.g. "Jan"), columns => length of the weeks array
          - row 1..7 => squares for Monday..Sunday
        We use calendar.monthcalendar(year, month), which yields e.g.
           [ [0,0,1,2,3,4,5],  # week1
             [6,7,8,9,10,11,12], # week2
             ...
           ]
        Each item is day-of-month or 0 if out of that month. Monday is index0, Sunday is index6.
        We'll produce #weeks columns in each row.
        """
        weeks = calendar.monthcalendar(year, month)
        # each week is [Mon, Tue, Wed, Thu, Fri, Sat, Sun], 0 if not in this month
        height = 8  # row0 => label, row1..7 => squares
        width = len(weeks)
        subgrid = [[" " for _ in range(width)] for _ in range(height)]

        # Put short month name in row0 (just at col0 for brevity)
        short_label = calendar.month_abbr[month]  # e.g. "Jan"
        label_chars = list(short_label)
        # place them starting col0
        for i, ch in enumerate(label_chars):
            if i < width:
                subgrid[0][i] = ch

        # Now fill squares for row=1..7, col= 0..width-1
        # weeks[w][d] => day-of-month or 0, d= 0..6 => Monday..Sunday
        for col in range(width):
            wdays = weeks[col]  # array of 7 days
            for dow in range(7):  # 0..6 => mon..sun
                day_num = wdays[dow]
                row = dow + 1  # row1 => Monday, row7 => Sunday
                if day_num == 0:
                    # blank => out of month
                    continue
                dt = datetime(year, month, day_num).date()
                c = date_counts.get(dt, 0)
                color = self._get_gradient_color(c, min_sub, max_sub, gradient)
                subgrid[row][col] = f"{color}{symbol}{self.ANSI_RESET}"

        return subgrid
