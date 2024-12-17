from leetcode_cli.graphics.ansi_codes import ANSI_CODES
from leetcode_cli.graphics.symbols import SYMBOLS

STATS_FORMATTER_DIFFICULTY_COLORS = {
    "EASY": ANSI_CODES["GREEN"],
    "MEDIUM": ANSI_CODES["ORANGE"],
    "HARD": ANSI_CODES["RED"],

    "CALENDAR_TIER0": ANSI_CODES["GRAY"],
    "CALENDAR_TIER1": ANSI_CODES["GREEN1"]
    # so on
}

STATS_FORMATTER_SYMBOLS = {
    "FILLED_SQUARE": SYMBOLS["FILLED_SQUARE"],
    "EMPTY_SQUARE": SYMBOLS["EMPTY_SQUARE"]
}
