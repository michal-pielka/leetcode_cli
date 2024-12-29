from leetcode_cli.graphics.ansi_codes import ANSI_RESET
from leetcode_cli.utils.theme_utils import load_theme_data
from leetcode_cli.models.problemset import ProblemSet, ProblemSummary
from leetcode_cli.exceptions.exceptions import ProblemSetFormatterError, ThemeError
import logging

logger = logging.getLogger(__name__)

class ProblemSetFormatter:
    def __init__(self, problemset: ProblemSet):
        self.problemset = problemset

        try:
            self.theme_data = load_theme_data()

        except ThemeError as e:
            raise ThemeError(f"Failed to load theme: {str(e)}")

    def _format_question(self, q: ProblemSummary) -> str:
        title = q.title.ljust(79)
        question_id = q.frontend_question_id.rjust(4)
        ac_rate = f"{float(q.ac_rate):.2f}"
        difficulty = q.difficulty
        status = q.status

        difficulty_ansi = self.theme_data['PROBLEMSET_FORMATTER_ANSI_CODES'].get(
            difficulty, ""
        )

        formatted_difficulty = f"{difficulty_ansi}{difficulty.ljust(8)}{ANSI_RESET}"

        status_symbol = self.theme_data['PROBLEMSET_FORMATTER_SYMBOLS'].get(
            status, ""
        )

        colored_status_symbol = (
            f"{self.theme_data['PROBLEMSET_FORMATTER_ANSI_CODES'].get(status, '')}"
            f"{status_symbol}"
            f"{ANSI_RESET}"
        )

        return f"\t{colored_status_symbol}[{question_id}] {title} {formatted_difficulty} ({ac_rate} %)"

    def get_formatted_questions(self) -> str:
        if not self.problemset.questions:
            logger.error("No questions available to format.")
            raise ProblemSetFormatterError("No questions available to format.")

        parsed_list = [self._format_question(q) for q in self.problemset.questions]

        return "\n".join(parsed_list)
