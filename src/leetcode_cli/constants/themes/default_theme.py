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

            # Shades of green for stats
            "GREEN1": "\u001b[38;2;1;155;1m",
            "GREEN2": "\u001b[38;2;16;175;16m",
            "GREEN3": "\u001b[38;2;33;195;33m",
            "GREEN4": "\u001b[38;2;61;215;61m",
            "GREEN5": "\u001b[38;2;82;235;82m",
            "GREEN6": "\u001b[38;2;100;255;100m",

            # Background colors
            "GRAY_BG": "\u001b[100m",
            "GREEN_BG": "\u001b[42m",
            "BABY_BLUE_BG": "\u001b[48;2;66;205;245m",
            "RED_BG": "\u001b[41m",
            "ORANGE_BG": "\u001b[48;2;245;158;66m",

            # Text styles
            "BOLD": "\u001b[1m",
            "ITALIC": "\u001b[3m",
            "UNDERLINE": "\u001b[4m",

            # For placeholders
            "EMPTY": ""
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
            "ATTEMPTED": "❋",
            "EMPTY": ""
        }
    },

    "mappings.json": {
        #
        # ─────────────────── INTERPRETATION ───────────────────
        #
        "INTERPRETATION_ANSI_CODES": {
            "Accepted": "GREEN,BOLD",
            "Wrong Answer": "RED,BOLD",
            "Memory Limit Exceeded": "RED,BOLD",
            "Output Limit Exceeded": "RED,BOLD",
            "Time Limit Exceeded": "RED,BOLD",
            "Runtime Error": "RED,BOLD",
            "Compile Error": "RED,BOLD",
            "unknown": "ORANGE,BOLD"
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
        },

        #
        # ─────────────────── PROBLEMSET ───────────────────
        #
        "PROBLEMSET_FORMATTER_ANSI_CODES": {
            "Easy": "GREEN",
            "Medium": "ORANGE",
            "Hard": "RED",
            "ac": "GREEN",
            "notac": "ORANGE",
            "not_started": "GRAY"
        },
        "PROBLEMSET_FORMATTER_SYMBOLS": {
            "Easy": "EMPTY",
            "Medium": "EMPTY",
            "Hard": "EMPTY",
            "ac": "CHECKMARK",
            "notac": "ATTEMPTED",
            "not_started": "ATTEMPTED"
        },

        #
        # ─────────────────── SUBMISSION ───────────────────
        #
        "SUBMISSION_ANSI_CODES": {
            "Accepted": "GREEN,BOLD",
            "Wrong Answer": "RED,BOLD",
            "Memory Limit Exceeded": "RED,BOLD",
            "Output Limit Exceeded": "RED,BOLD",
            "Time Limit Exceeded": "RED,BOLD",
            "Runtime Error": "RED,BOLD",
            "Compile Error": "RED,BOLD",
            "unknown": "ORANGE,BOLD"
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
        },

        #
        # ─────────────────── PROBLEM FORMATTER ───────────────────
        #
        "PROBLEM_FORMATTER_ANSI_CODES": {
            "strong": "BOLD",
            "p": "EMPTY",
            "br": "EMPTY",
            "ul": "EMPTY",
            "li": "EMPTY",
            "sup": "EMPTY",
            "b": "BOLD",
            "em": "ITALIC",
            "i": "ITALIC",
            "u": "UNDERLINE",
            "code": "GRAY_BG",
            "pre": "RED",
            "tag": "BABY_BLUE_BG,WHITE,BOLD",
            "language": "ORANGE_BG,BLACK,BOLD",
            "title": "BOLD",
            "Easy": "GREEN",
            "Medium": "ORANGE",
            "Hard": "RED",
            "example_title": "BOLD",
            "example_input_string": "BOLD",
            "example_output_string": "BOLD",
            "example_explanation_string": "BOLD",
            "example_input_data": "GRAY",
            "example_output_data": "GRAY",
            "example_explanation_data": "GRAY",
            "constraints_string": "BOLD"
        },
        "PROBLEM_FORMATTER_SYMBOLS": {
            "strong": "EMPTY",
            "p": "EMPTY",
            "br": "EMPTY",
            "ul": "EMPTY",
            "li": "DOT",
            "sup": "CARET",
            "b": "EMPTY",
            "em": "EMPTY",
            "i": "EMPTY",
            "u": "EMPTY",
            "code": "EMPTY",
            "pre": "EMPTY",
            "tag": "EMPTY",
            "language": "EMPTY",
            "title": "EMPTY",
            "Easy": "EMPTY",
            "Medium": "EMPTY",
            "Hard": "EMPTY",
            "example_title": "EMPTY",
            "example_input_string": "EMPTY",
            "example_output_string": "EMPTY",
            "example_explanation_string": "EMPTY",
            "example_input_data": "EMPTY",
            "example_output_data": "EMPTY",
            "example_explanation_data": "EMPTY",
            "constraints_string": "EMPTY"
        },

        #
        # ─────────────────── STATS FORMATTER ───────────────────
        #
        "STATS_FORMATTER_DIFFICULTY_COLORS": {
            "EASY": "GREEN",
            "MEDIUM": "ORANGE",
            "HARD": "RED",
            "CALENDAR_TIER0": "GRAY"
        },
        "STATS_FORMATTER_SYMBOLS": {
            "EASY": "EMPTY",
            "MEDIUM": "EMPTY",
            "HARD": "EMPTY",
            "CALENDAR_TIER0": "EMPTY",
            "FILLED_SQUARE": "FILLED_SQUARE",
            "EMPTY_SQUARE": "EMPTY_SQUARE"
        }
    }
}
