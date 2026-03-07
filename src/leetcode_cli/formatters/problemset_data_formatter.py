import logging

from leetcode_cli.managers.theme_manager import ThemeManager
from leetcode_cli.models.problemset import ProblemSet, ProblemSummary

logger = logging.getLogger(__name__)


class ProblemSetFormatterError(Exception):
    """Custom exception for ProblemSetFormatter errors."""

    pass


class ProblemSetFormatter:
    """
    Formats problem listings using theme styling.

    Format:
        {paid}{status}[{question_id}] {title} {difficulty} ({ac_rate}%)
    """

    def __init__(self, problemset: ProblemSet, theme_manager: ThemeManager):
        self.problemset = problemset
        self.theme_manager = theme_manager
        self.theme_data = self.theme_manager.load_theme_data()

        self.ANSI_RESET = "\033[0m"

    def _format_question(self, q: ProblemSummary) -> str:
        title = q.title.ljust(79)
        title_ansi, _ = self.theme_manager.get_styling("text", "title")
        formatted_title = f"{title_ansi}{title}{self.ANSI_RESET}"

        question_id = q.frontend_question_id.rjust(4)
        id_ansi, _ = self.theme_manager.get_styling("text", "question_id")
        formatted_question_id = f"{id_ansi}[{question_id}]{self.ANSI_RESET}"

        ac_rate = f"{float(q.ac_rate):.2f}"
        ac_ansi, _ = self.theme_manager.get_styling("text", "ac_rate")
        formatted_ac_rate = f"{ac_ansi}({ac_rate}%){self.ANSI_RESET}"

        diff_key = q.difficulty.lower()
        diff_ansi, _ = self.theme_manager.get_styling("difficulty", diff_key)
        padded_diff = q.difficulty.ljust(8)
        formatted_difficulty = f"{diff_ansi}{padded_diff}{self.ANSI_RESET}"

        status_key = q.status.lower() if q.status else "not_started"
        status_ansi, status_icon = self.theme_manager.get_styling("status", status_key)
        formatted_status = f"{status_ansi}{status_icon}{self.ANSI_RESET}"

        is_paid_key = "paid_only" if q.paid_only else "not_paid_only"
        paid_ansi, paid_icon = self.theme_manager.get_styling("paid", is_paid_key)
        formatted_paid = f"{paid_ansi}{paid_icon}{self.ANSI_RESET}"

        # Pad icon fields to consistent width
        if not status_icon:
            formatted_status = " "
        if not paid_icon:
            formatted_paid = " "

        line = (
            f"\t{formatted_paid}"
            f"{formatted_status}"
            f"{formatted_question_id} "
            f"{formatted_title} "
            f" {formatted_difficulty} "
            f"{formatted_ac_rate}"
        )
        return line

    def get_formatted_questions(self) -> str:
        if not self.problemset.questions:
            logger.error("No questions available to format.")
            raise ProblemSetFormatterError("No questions available to format.")

        lines = [self._format_question(q) for q in self.problemset.questions]
        return "\n".join(lines)
