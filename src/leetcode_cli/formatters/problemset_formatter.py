# leetcode_cli/formatters/problemset_formatter.py
from leetcode_cli.graphics.ansi_codes import ANSI_RESET
from leetcode_cli.utils.theme_utils import get_theme_data
from leetcode_cli.models.problemset import ProblemSet, ProblemSummary
from leetcode_cli.exceptions.exceptions import ProblemSetFormatterError

import logging

logger = logging.getLogger(__name__)

class ProblemSetFormatter:

    def __init__(self, problemset: ProblemSet):
        if not isinstance(problemset, ProblemSet):
            raise ProblemSetFormatterError("ProblemSetFormatter requires a ProblemSet instance.")
        self.problemset = problemset
        self.THEME_DATA = get_theme_data()

    def _format_question(self, q: ProblemSummary) -> str:
        title = q.title.ljust(79)
        question_id = q.frontend_question_id.rjust(4)
        ac_rate = f"{float(q.ac_rate):.2f}"
        difficulty = q.difficulty
        status = q.status

        formatted_difficulty = f"{self.THEME_DATA['PROBLEMSET_FORMATTER_ANSI_CODES'].get(difficulty, '')}{difficulty.ljust(8)}{ANSI_RESET}"
        status_symbol = self.THEME_DATA['PROBLEMSET_FORMATTER_SYMBOLS'].get(status, " ")
        colored_status_symbol = f"{self.THEME_DATA['PROBLEMSET_FORMATTER_ANSI_CODES'].get(status, '')}{status_symbol}{ANSI_RESET}"

        return f"\t{colored_status_symbol}[{question_id}] {title} {formatted_difficulty} ({ac_rate} %)"

    def get_formatted_questions(self) -> str:
        if not self.problemset.questions:
            logger.error("No questions available to format.")
            raise ProblemSetFormatterError("No questions available to format.")

        parsed_list = [self._format_question(q) for q in self.problemset.questions]
        return "\n".join(parsed_list)
