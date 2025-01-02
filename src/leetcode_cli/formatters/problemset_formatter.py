import logging

from leetcode_cli.graphics.ansi_codes import ANSI_RESET
from leetcode_cli.models.problemset import ProblemSet, ProblemSummary
from leetcode_cli.exceptions.exceptions import ProblemSetFormatterError
from leetcode_cli.services.theme_service import get_styling
from leetcode_cli.models.theme import ThemeData
from leetcode_cli.exceptions.exceptions import ThemeError

logger = logging.getLogger(__name__)


class ProblemSetFormatter:
    """
    Formats and styles the list of problems in the problem set using theme mappings.
    """

    def __init__(self, problemset: ProblemSet, theme_data: ThemeData):
        self.problemset = problemset
        self.theme_data = theme_data

    def _format_question(self, q: ProblemSummary) -> str:
        """
        Formats a single problem entry with appropriate styling.

        :param q: The ProblemSummary object representing a single problem.
        :return: A formatted string representing the styled problem entry.
        """
        try:
            title_ansi, title_symbol = get_styling(self.theme_data, 'PROBLEMSET', 'title')
            formatted_title = q.title.ljust(80)
            styled_title = f"{title_ansi}{title_symbol}{formatted_title}{ANSI_RESET}"

            qid_ansi, qid_symbol = get_styling(self.theme_data, 'PROBLEMSET', 'question_id')
            formatted_qid = f"{q.frontend_question_id:>4}"
            id_with_brackets = f"[{formatted_qid}]"
            styled_id = f"{qid_ansi}{qid_symbol}{id_with_brackets}{ANSI_RESET}"

            ac_rate_ansi, ac_rate_symbol = get_styling(self.theme_data, 'PROBLEMSET', 'ac_rate')
            formatted_ac_rate = f"{float(q.ac_rate):.2f}%"
            styled_ac_rate = f"{ac_rate_ansi}{ac_rate_symbol}{formatted_ac_rate}{ANSI_RESET}"

            difficulty_key = q.difficulty.capitalize()
            diff_ansi, diff_symbol = get_styling(self.theme_data, 'PROBLEMSET', difficulty_key)
            styled_difficulty = f"{diff_ansi}{diff_symbol}{difficulty_key}{ANSI_RESET}"
            difficulty_padding = ' ' * (8 - len(difficulty_key))
            styled_difficulty += difficulty_padding

            status_key = q.status.lower() if q.status else 'not_started'
            status_ansi, status_symbol = get_styling(self.theme_data, 'PROBLEMSET', status_key)
            colored_status_symbol = f"{status_ansi}{status_symbol}{ANSI_RESET}"

            formatted_question = (
                f"\t{colored_status_symbol} {styled_id} {styled_title} "
                f"{styled_difficulty} ({styled_ac_rate})"
            )

            return formatted_question

        except ThemeError as te:
            logger.error(f"Theming Error in _format_question: {te}")
            raise te

    def get_formatted_questions(self) -> str:
        """
        Formats the entire list of problems in the problem set.

        :return: A string containing all formatted and styled problem entries.
        """
        if not self.problemset.questions:
            logger.error("No questions available to format.")
            raise ProblemSetFormatterError("No questions available to format.")

        try:
            parsed_list = [self._format_question(q) for q in self.problemset.questions]

        except ThemeError as te:
            logger.error(f"Theming Error in get_formatted_questions: {te}")
            raise te

        return "\n".join(parsed_list)
