import logging

from leetcode_cli.graphics.ansi_codes import ANSI_RESET
from leetcode_cli.models.problemset import ProblemSet, ProblemSummary
from leetcode_cli.exceptions.exceptions import ProblemSetFormatterError
from leetcode_cli.services.theme_service import get_ansi_code, get_symbol
from leetcode_cli.models.theme import ThemeData

logger = logging.getLogger(__name__)

class ProblemSetFormatter:
    def __init__(self, problemset: ProblemSet, theme_data: ThemeData):
        self.problemset = problemset
        self.theme_data = theme_data

    def _format_question(self, q: ProblemSummary) -> str:
        title = q.title.ljust(79)
        question_id = q.frontend_question_id.rjust(4)
        ac_rate = f"{float(q.ac_rate):.2f}"
        difficulty = q.difficulty
        status = q.status or "not_started"

        difficulty_ansi = get_ansi_code(self.theme_data, 'PROBLEMSET_FORMATTER_ANSI_CODES', difficulty)
        formatted_difficulty = f"{difficulty_ansi}{difficulty.ljust(8)}{ANSI_RESET}"

        status_symbol = get_symbol(self.theme_data, 'PROBLEMSET_FORMATTER_SYMBOLS', status)
        status_color = get_ansi_code(self.theme_data, 'PROBLEMSET_FORMATTER_ANSI_CODES', status)
        colored_status_symbol = f"{status_color}{status_symbol}{ANSI_RESET}"

        return f"\t{colored_status_symbol}[{question_id}] {title} {formatted_difficulty} ({ac_rate} %)"

    def get_formatted_questions(self) -> str:
        if not self.problemset.questions:
            logger.error("No questions available to format.")
            raise ProblemSetFormatterError("No questions available to format.")

        parsed_list = [self._format_question(q) for q in self.problemset.questions]
        return "\n".join(parsed_list)
