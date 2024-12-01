
from ..graphics.escape_sequences import ANSI_CODES, ANSI_RESET
from ..graphics.symbols import SYMBOLS

class LeetCodeProblemsetParser:
    DIFFICULTY_TO_ANSI = {
        "Easy" : ANSI_CODES["GREEN"],
        "Medium" : ANSI_CODES["ORANGE"],
        "Hard" : ANSI_CODES["RED"]
    }

    QUESTION_STATUS_TO_COLORED_SYMBOL = {
        "ac" : ANSI_CODES["GREEN"] + SYMBOLS["CHECKMARK"] + ANSI_RESET,
        "notac" : ANSI_CODES["ORANGE"] + SYMBOLS["ATTEMPTED"] + ANSI_RESET,
        #None: ANSI_CODES["RED"] + SYMBOLS["X"] + ANSI_RESET
        None: " "
    }

    def __init__(self, problemset_metadata):
        self.problemset_metadata = problemset_metadata

        print(problemset_metadata)
        self.problemset_data = self.problemset_metadata.get("data", None)

        self.problemset_question_list = self.problemset_data.get("problemsetQuestionList", None)
        self.total_problems = self.problemset_question_list.get("total", None)
        self.questions = self.problemset_question_list.get("questions", None)

    def _parse_question(self, question_data):
        title = question_data.get("title", "").ljust(79)  # Adjust width for title alignment
        question_id = str(question_data.get("frontendQuestionId", "")).rjust(4)  # Align ID for up to 4 digits
        acceptance_rate = f"{float(question_data.get('acRate', 0)):.2f}"  # Format acceptance rate with two decimals
        difficulty = question_data.get("difficulty", "")
        status = question_data.get("status", None)
        # Colorize and align difficulty
        formatted_difficulty = f"{self.DIFFICULTY_TO_ANSI[difficulty]}{difficulty.ljust(8)}{ANSI_RESET}"

        # Combine all parts into a formatted string
        
        parsed_question = f"\t{self.QUESTION_STATUS_TO_COLORED_SYMBOL[status]}[{question_id}] {title} {formatted_difficulty} ({acceptance_rate} %)"
        return parsed_question

    def parse_questions(self):
        parsed_string = ""

        for question in self.questions:
            parsed_question = self._parse_question(question)
            parsed_string += parsed_question
            parsed_string += "\n"

        return parsed_string
        
        

