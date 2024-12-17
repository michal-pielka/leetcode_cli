from leetcode_cli.graphics.ansi_codes import ANSI_CODES
from leetcode_cli.graphics.symbols import SYMBOLS

PROBLEMSET_FORMATTER_ANSI_CODES = {
    "Easy": ANSI_CODES["GREEN"],
    "Medium": ANSI_CODES["ORANGE"],
    "Hard": ANSI_CODES["RED"],
    "ac": ANSI_CODES["GREEN"],
    "notac": ANSI_CODES["ORANGE"],
}

PROBLEMSET_FORMATTER_SYMBOLS = {
    "ac": SYMBOLS["CHECKMARK"],
    "notac": SYMBOLS["ATTEMPTED"],
}
