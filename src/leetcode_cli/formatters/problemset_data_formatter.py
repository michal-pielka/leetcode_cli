import logging

from leetcode_cli.models.problemset import ProblemSet, ProblemSummary
from leetcode_cli.exceptions.exceptions import FormattingError, ThemeError
from leetcode_cli.managers.theme_manager import ThemeManager

logger = logging.getLogger(__name__)

class ProblemSetFormatterError(Exception):
    """Custom exception for ProblemSetFormatter errors."""
    pass

class ProblemSetFormatter:
    """
    Replicates the original 'column-based' formatting of problem listings
    but uses theme data (from ThemeManager) for coloring and symbols.

    Format example (unchanged):
        \t{status_symbol}[{question_id}] {title} {difficulty} ({ac_rate} %)
    
    where:
      - {question_id} is right-justified in 4 spaces
      - {title} is left-justified with padding of 79 spaces
      - {difficulty} is left-justified with padding of 8 spaces
      - {ac_rate} is a floating percentage
    """

    def __init__(self, problemset: ProblemSet, theme_manager: ThemeManager):
        self.problemset = problemset
        self.theme_manager = theme_manager
        self.theme_data = self.theme_manager.load_theme_data()

        self.ANSI_RESET = "\033[0m"       # Reset all styles

    def _format_question(self, q: ProblemSummary) -> str:
        """
        Formats a single problem with spacing identical to the original code snippet.
        """
        # Title padded to 79 characters
        title = q.title.ljust(79)
        title_ansi, title_left, title_right = self.theme_manager.get_styling("PROBLEMSET", "title")
        formatted_title =  f"{title_ansi}{title_left}{title}{title_right}{self.ANSI_RESET}"

        question_id = q.frontend_question_id.rjust(4)
        id_ansi, id_left, id_right = self.theme_manager.get_styling("PROBLEMSET", "question_id")
        formatted_question_id = f"{id_ansi}{id_left}{question_id}{id_right}{self.ANSI_RESET}"

        ac_rate = f"{float(q.ac_rate):.2f}"
        ac_ansi, ac_left, ac_right = self.theme_manager.get_styling("PROBLEMSET", "acceptance_rate")
        formatted_ac_rate = f"{ac_ansi}{ac_left}{ac_rate}{ac_right}{self.ANSI_RESET}"

        difficulty_str = q.difficulty
        diff_key = difficulty_str.capitalize()  # e.g., "Easy", "Medium", "Hard"
        try:
            diff_ansi, diff_left, diff_right = self.theme_manager.get_styling("PROBLEMSET", diff_key)

        except ThemeError as te:
            raise te

        padded_diff = difficulty_str.ljust(8)
        formatted_difficulty = f"{diff_ansi}{diff_left}{padded_diff}{diff_right}{self.ANSI_RESET}"

        status_key = (q.status.lower() if q.status else "not_started")
        try:
            status_ansi, status_left, status_right = self.theme_manager.get_styling("PROBLEMSET", status_key)

        except ThemeError as te:
            raise te

        formatted_status_symbol = f"{status_ansi}{status_left}{status_right}{self.ANSI_RESET}"

        line = (
            f"\t{formatted_status_symbol}"             # e.g. "\t✔"
            f"{formatted_question_id} "             # e.g. "[ 299]" (4 digits right-justified)
            f"{formatted_title} "                      # 79-char-ljust title
            f" {formatted_difficulty} "      # e.g. "Easy    " with theming
            f"{formatted_ac_rate}"                # e.g. "(53.45 %)"
        )
        return line

    def get_formatted_questions(self) -> str:
        """
        Returns a formatted string of all problems in the problemset, 
        matching the old spacing & alignment, but theming is applied.
        """
        if not self.problemset.questions:
            logger.error("No questions available to format.")
            raise ProblemSetFormatterError("No questions available to format.")

        lines = [self._format_question(q) for q in self.problemset.questions]
        return "\n".join(lines)
