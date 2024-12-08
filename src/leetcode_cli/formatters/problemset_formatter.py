from leetcode_cli.graphics.escape_sequences import ANSI_CODES, ANSI_RESET
from leetcode_cli.graphics.symbols import SYMBOLS
import logging
from leetcode_cli.models.problemset import ProblemSet, ProblemSummary

logger = logging.getLogger(__name__)

class ProblemSetFormatterError(Exception):
    """Custom exception for ProblemSetFormatter errors."""
    pass

class ProblemSetFormatter:
    DIFFICULTY_TO_ANSI = {
        "Easy": ANSI_CODES["GREEN"],
        "Medium": ANSI_CODES["ORANGE"],
        "Hard": ANSI_CODES["RED"]
    }

    QUESTION_STATUS_TO_COLORED_SYMBOL = {
        "ac": ANSI_CODES["GREEN"] + SYMBOLS["CHECKMARK"] + ANSI_RESET,
        "notac": ANSI_CODES["ORANGE"] + SYMBOLS["ATTEMPTED"] + ANSI_RESET,
        None: " "
    }

    def __init__(self, problemset: ProblemSet):
        if not isinstance(problemset, ProblemSet):
            raise ProblemSetFormatterError("ProblemSetFormatter requires a ProblemSet instance.")
        self.problemset = problemset

    def _format_question(self, q: ProblemSummary) -> str:
        title = q.title.ljust(79)  # Adjust width for alignment
        question_id = q.frontend_question_id.rjust(4)  # align ID for up to 4 digits
        ac_rate = f"{float(q.ac_rate):.2f}"  # format acceptance rate
        difficulty = q.difficulty
        status = q.status

        # Colorize difficulty
        formatted_difficulty = f"{self.DIFFICULTY_TO_ANSI.get(difficulty, '')}{difficulty.ljust(8)}{ANSI_RESET}"

        # Status symbol
        status_symbol = self.QUESTION_STATUS_TO_COLORED_SYMBOL.get(status, " ")

        # Combine into a formatted string
        # Example format:
        #    [  1] Two Sum                                                                        Easy     (54.34 %)
        return f"\t{status_symbol}[{question_id}] {title} {formatted_difficulty} ({ac_rate} %)"

    def get_formatted_questions(self) -> str:
        """
        Returns a formatted string of all problems in the problemset.
        """
        if not self.problemset.questions:
            logger.error("No questions available to format.")
            raise ProblemSetFormatterError("No questions available to format.")

        parsed_list = [self._format_question(q) for q in self.problemset.questions]
        return "\n".join(parsed_list)
