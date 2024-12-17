from leetcode_cli.graphics.ansi_codes import ANSI_CODES
from leetcode_cli.graphics.symbols import SYMBOLS

SUBMISSION_ANSI_CODES = {
    "Accepted": ANSI_CODES["GREEN"] + ANSI_CODES["BOLD"],
    "Wrong Answer": ANSI_CODES["RED"] + ANSI_CODES["BOLD"],
    "Memory Limit Exceeded": ANSI_CODES["RED"] + ANSI_CODES["BOLD"],
    "Output Limit Exceeded": ANSI_CODES["RED"] + ANSI_CODES["BOLD"],
    "Time Limit Exceeded": ANSI_CODES["RED"] + ANSI_CODES["BOLD"],
    "Runtime Error": ANSI_CODES["RED"] + ANSI_CODES["BOLD"],
    "Compile Error": ANSI_CODES["RED"] + ANSI_CODES["BOLD"],
    "unknown": ANSI_CODES["ORANGE"] + ANSI_CODES["BOLD"],
}

SUBMISSION_SYMBOLS = {
    "Accepted": SYMBOLS["CHECKMARK"],
    "Wrong Answer": SYMBOLS["X"],
    "Memory Limit Exceeded": SYMBOLS["X"],
    "Output Limit Exceeded": SYMBOLS["X"],
    "Time Limit Exceeded": SYMBOLS["X"],
    "Runtime Error": SYMBOLS["X"],
    "Compile Error": SYMBOLS["X"],
    "unknown": SYMBOLS["X"],
}
