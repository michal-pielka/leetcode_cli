DEFAULT_THEME_FILES = {
    "ansi_codes.json": {
        "ANSI_CODES": {
            "RESET": "\u001b[0m",
            "GREEN": "\u001b[32m",
            "ORANGE": "\u001b[38;5;208m",
            "RED": "\u001b[31m",
            "GRAY": "\u001b[90m",
            "CYAN": "\u001b[96m",
            "WHITE": "\u001b[38;2;255;255;255m",
            "BLACK": "\u001b[38;2;0;0;0m",
            "GREEN1": "\u001b[38;2;1;155;1m",
            "GREEN2": "\u001b[38;2;16;175;16m",
            "GREEN3": "\u001b[38;2;33;195;33m",
            "GREEN4": "\u001b[38;2;61;215;61m",
            "GREEN5": "\u001b[38;2;82;235;82m",
            "GREEN6": "\u001b[38;2;100;255;100m",
            "GRAY_BG": "\u001b[100m",
            "GREEN_BG": "\u001b[42m",
            "BABY_BLUE_BG": "\u001b[48;2;66;205;245m",
            "RED_BG": "\u001b[41m",
            "ORANGE_BG": "\u001b[48;2;245;158;66m",
            "BOLD": "\u001b[1m",
            "ITALIC": "\u001b[3m",
            "UNDERLINE": "\u001b[4m"
        }
    },
    "symbols.json": {
        "SYMBOLS": {
            "FILLED_SQUARE": "◼",
            "EMPTY_SQUARE": "▫",
            "CARET": "^",
            "DOT": "•",
            "CHECKMARK": "✔",
            "X": "✘",
            "ATTEMPTED": "❋"
        }
    },
    "interpretation_mappings.json": {
        # References to ANSI_CODES and SYMBOLS by their keys
        "INTERPRETATION_ANSI_CODES": {
            "Accepted": "GREEN BOLD",    # "GREEN" and "BOLD" can be combined by theme_utils if needed.
            "Wrong Answer": "RED BOLD",
            "Memory Limit Exceeded": "RED BOLD",
            "Output Limit Exceeded": "RED BOLD",
            "Time Limit Exceeded": "RED BOLD",
            "Runtime Error": "RED BOLD",
            "Compile Error": "RED BOLD",
            "unknown": "ORANGE BOLD"
        },
        "INTERPRETATION_SYMBOLS": {
            "Accepted": "CHECKMARK",
            "Wrong Answer": "X",
            "Memory Limit Exceeded": "X",
            "Output Limit Exceeded": "X",
            "Time Limit Exceeded": "X",
            "Runtime Error": "X",
            "Compile Error": "X",
            "unknown": "X"
        }
    },
    "problemset_mappings.json": {
        "PROBLEMSET_FORMATTER_ANSI_CODES": {
            "Easy": "GREEN",
            "Medium": "ORANGE",
            "Hard": "RED",
            "ac": "GREEN",
            "notac": "ORANGE"
        },
        "PROBLEMSET_FORMATTER_SYMBOLS": {
            "ac": "CHECKMARK",
            "notac": "ATTEMPTED"
        }
    },
    "submission_mappings.json": {
        "SUBMISSION_ANSI_CODES": {
            "Accepted": "GREEN BOLD",
            "Wrong Answer": "RED BOLD",
            "Memory Limit Exceeded": "RED BOLD",
            "Output Limit Exceeded": "RED BOLD",
            "Time Limit Exceeded": "RED BOLD",
            "Runtime Error": "RED BOLD",
            "Compile Error": "RED BOLD",
            "unknown": "ORANGE BOLD"
        },
        "SUBMISSION_SYMBOLS": {
            "Accepted": "CHECKMARK",
            "Wrong Answer": "X",
            "Memory Limit Exceeded": "X",
            "Output Limit Exceeded": "X",
            "Time Limit Exceeded": "X",
            "Runtime Error": "X",
            "Compile Error": "X",
            "unknown": "X"
        }
    },
    "problem_mappings.json": {
        # Values here are keys that reference ANSI_CODES or SYMBOLS
        # For compound styles like "GREEN BOLD", the theme_utils would need logic to parse and combine.
        "PROBLEM_FORMATTER_ANSI_CODES": {
            "strong": "BOLD",
            "b": "BOLD",
            "em": "ITALIC",
            "i": "ITALIC",
            "u": "UNDERLINE",
            "code": "GRAY_BG",
            "pre": "RED",
            "tag": "BABY_BLUE_BG WHITE BOLD",
            "language": "ORANGE_BG BLACK BOLD",
            "title": "BOLD",
            "example_title": "BOLD",
            "example_input_string": "BOLD",
            "example_output_string": "BOLD",
            "example_explanation_string": "BOLD",
            "example_input_data": "GRAY",
            "example_output_data": "GRAY",
            "example_explanation_data": "GRAY",
            "constraints_string": "BOLD",
            "Easy": "GREEN_BG",
            "Medium": "ORANGE_BG",
            "Hard": "RED_BG"
        },
        "PROBLEM_FORMATTER_SYMBOLS": {
            "sup": "CARET",
            "li": "DOT"
        }
    },
    "stats_mappings.json": {
        "STATS_FORMATTER_DIFFICULTY_COLORS": {
            "EASY": "GREEN",
            "MEDIUM": "ORANGE",
            "HARD": "RED",
            "CALENDAR_TIER0": "GRAY",
            "CALENDAR_TIER1": "GREEN1"
        },
        "STATS_FORMATTER_SYMBOLS": {
            "FILLED_SQUARE": "FILLED_SQUARE",
            "EMPTY_SQUARE": "EMPTY_SQUARE"
        }
    }
}
