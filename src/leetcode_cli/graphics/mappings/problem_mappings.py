from leetcode_cli.graphics.symbols import SYMBOLS
from leetcode_cli.graphics.ansi_codes import ANSI_CODES

# Problem description formatting
PROBLEM_FORMATTER_ANSI_CODES = {
    "strong": ANSI_CODES["BOLD"],
    "b": ANSI_CODES["BOLD"],
    "em": ANSI_CODES["ITALIC"],
    "i": ANSI_CODES["ITALIC"],
    "u": ANSI_CODES["UNDERLINE"],
    "code": ANSI_CODES["GRAY_BG"],
    "pre": ANSI_CODES["RED"],
    "tag": ANSI_CODES["BABY_BLUE_BG"] + ANSI_CODES["WHITE"] + ANSI_CODES["BOLD"],
    "language": ANSI_CODES["ORANGE_BG"] + ANSI_CODES["BLACK"] + ANSI_CODES["BOLD"],
    "title": ANSI_CODES["BOLD"],
    "example_title": ANSI_CODES["BOLD"],
    "example_input_string": ANSI_CODES["BOLD"],
    "example_output_string": ANSI_CODES["BOLD"],
    "example_explanation_string": ANSI_CODES["BOLD"],
    "example_input_data": ANSI_CODES["GRAY"],
    "example_output_data": ANSI_CODES["GRAY"],
    "example_explanation_data": ANSI_CODES["GRAY"],
    "constraints_string": ANSI_CODES["BOLD"],
    "Easy": ANSI_CODES["GREEN_BG"],
    "Medium": ANSI_CODES["ORANGE_BG"],
    "Hard": ANSI_CODES["RED_BG"],
}

PROBLEM_FORMATTER_SYMBOLS = {
    "sup": SYMBOLS["CARET"],
    "li": SYMBOLS["DOT"] + " ",
}

