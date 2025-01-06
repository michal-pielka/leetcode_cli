import logging

from leetcode_cli.graphics.ansi_codes import ANSI_RESET
from leetcode_cli.models.problemset import ProblemSet, ProblemSummary
from leetcode_cli.exceptions.exceptions import FormattingError
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
            # Title Styling
            title_ansi, title_symbol_left, title_symbol_right = get_styling(self.theme_data, 'PROBLEMSET', 'title')
            formatted_title = q.title.ljust(80)
            styled_title = f"{title_ansi}{title_symbol_left}{formatted_title}{title_symbol_right}{ANSI_RESET}"

            # Question ID Styling
            qid_ansi, qid_symbol_left, qid_symbol_right = get_styling(self.theme_data, 'PROBLEMSET', 'question_id')
            formatted_qid = f"{q.frontend_question_id:>4}"
            id_with_brackets = f"{qid_symbol_left}{formatted_qid}{qid_symbol_right}"
            styled_id = f"{qid_ansi}{id_with_brackets}{ANSI_RESET}"

            # Acceptance Rate Styling
            ac_rate_ansi, ac_rate_symbol_left, ac_rate_symbol_right = get_styling(self.theme_data, 'PROBLEMSET', 'acceptance_rate')
            formatted_ac_rate = f"{float(q.ac_rate):.2f}"
            styled_ac_rate = f"{ac_rate_ansi}{ac_rate_symbol_left}{formatted_ac_rate}{ac_rate_symbol_right}{ANSI_RESET}"

            # Difficulty Styling
            difficulty_key = q.difficulty.capitalize()
            diff_ansi, diff_symbol_left, diff_symbol_right = get_styling(self.theme_data, 'PROBLEMSET', difficulty_key)
            styled_difficulty = f"{diff_ansi}{diff_symbol_left}{difficulty_key}{diff_symbol_right}{ANSI_RESET}"
            difficulty_padding = ' ' * (8 - len(difficulty_key))
            styled_difficulty += difficulty_padding

            # Status Styling
            status_key = q.status.lower() if q.status else 'not_started'
            status_ansi, status_symbol_left, status_symbol_right = get_styling(self.theme_data, 'PROBLEMSET', status_key)

            # Default to white if ansi_code is empty
            if not status_ansi:
                status_ansi = self.theme_data.ANSI_CODES.get("white", "")

            colored_status_symbol = f"{status_ansi}{status_symbol_left}{status_symbol_right}{ANSI_RESET}"

            # Combine all parts with proper styling
            formatted_question = (
                f"\t{colored_status_symbol}{styled_id} {styled_title} "
                f"{styled_difficulty} {styled_ac_rate}"
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
            raise FormattingError("No questions available to format.")

        try:
            parsed_list = [self._format_question(q) for q in self.problemset.questions]

        except ThemeError as te:
            logger.error(f"Theming Error in get_formatted_questions: {te}")
            raise te

        return "\n".join(parsed_list)
