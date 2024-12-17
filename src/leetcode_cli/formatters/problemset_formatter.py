from leetcode_cli.graphics.ansi_codes import ANSI_RESET
from leetcode_cli.graphics.mappings.problemset_mappings import PROBLEMSET_FORMATTER_SYMBOLS, PROBLEMSET_FORMATTER_ANSI_CODES
from leetcode_cli.models.problemset import ProblemSet, ProblemSummary
from leetcode_cli.exceptions.exceptions import ProblemSetFormatterError

import logging

logger = logging.getLogger(__name__)

class ProblemSetFormatter:

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
        formatted_difficulty = f"{PROBLEMSET_FORMATTER_ANSI_CODES.get(difficulty, '')}{difficulty.ljust(8)}{ANSI_RESET}"

        # Status symbol
        status_symbol = PROBLEMSET_FORMATTER_SYMBOLS.get(status, " ")
        colored_status_symbol = f"{PROBLEMSET_FORMATTER_ANSI_CODES.get(status, "")}{status_symbol}{ANSI_RESET}"

        # Combine into a formatted string
        # Example format:
        #    [  1] Two Sum                                                                        Easy     (54.34 %)
        return f"\t{colored_status_symbol}[{question_id}] {title} {formatted_difficulty} ({ac_rate} %)"

    def get_formatted_questions(self) -> str:
        """
        Returns a formatted string of all problems in the problemset.
        """
        if not self.problemset.questions:
            logger.error("No questions available to format.")
            raise ProblemSetFormatterError("No questions available to format.")

        parsed_list = [self._format_question(q) for q in self.problemset.questions]
        return "\n".join(parsed_list)
