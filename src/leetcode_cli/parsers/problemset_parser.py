from leetcode_cli.graphics.escape_sequences import ANSI_CODES, ANSI_RESET
from leetcode_cli.graphics.symbols import SYMBOLS
import logging

logger = logging.getLogger(__name__)

class LeetCodeProblemsetParserError(Exception):
    """Custom exception for LeetCodeProblemsetParser errors."""
    pass

class LeetCodeProblemsetParser:
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

    def __init__(self, questions_data):
        self.questions_data = questions_data

    def _parse_question(self, question_data):
        title = question_data.get("title", "").ljust(79)  # Adjust width for title alignment
        question_id = str(question_data.get("frontendQuestionId", "")).rjust(4)  # Align ID for up to 4 digits
        acceptance_rate = f"{float(question_data.get('acRate', 0)):.2f}"  # Format acceptance rate with two decimals
        difficulty = question_data.get("difficulty", "")
        status = question_data.get("status", None)
        # Colorize and align difficulty
        formatted_difficulty = f"{self.DIFFICULTY_TO_ANSI.get(difficulty, '')}{difficulty.ljust(8)}{ANSI_RESET}"

        # Combine all parts into a formatted string

        parsed_question = f"\t{self.QUESTION_STATUS_TO_COLORED_SYMBOL.get(status, ' ')}[{question_id}] {title} {formatted_difficulty} ({acceptance_rate} %)"
        return parsed_question

    def get_formatted_questions(self):
        """
        Formats the list of questions.

        Returns:
            str: A formatted string of questions.

        Raises:
            LeetCodeProblemsetParserError: If questions data is invalid.
        """
        if not self.questions_data:
            logger.error("No questions available to parse.")
            raise LeetCodeProblemsetParserError("No questions available to parse.")

        parsed_list = []

        for question in self.questions_data:
            parsed_question = self._parse_question(question)
            parsed_list.append(parsed_question)

        return "\n".join(parsed_list)
