from bs4 import BeautifulSoup, NavigableString, Tag

from leetcode_cli.graphics.escape_sequences import ANSI_CODES, ANSI_RESET
from leetcode_cli.graphics.symbols import SYMBOLS

class ProblemFormatter:
    HTML_TO_ANSI = {
        "strong": ANSI_CODES["BOLD"],
        "b": ANSI_CODES["BOLD"],
        "em": ANSI_CODES["ITALIC"],
        "i": ANSI_CODES["ITALIC"],
        "u": ANSI_CODES["UNDERLINE"],
        "code": ANSI_CODES["GRAY_BG"],
        "pre": ANSI_CODES["RED"],
        "tag": ANSI_CODES["BABY_BLUE_BG"] + ANSI_CODES["WHITE"] + ANSI_CODES["BOLD"],
        "language": ANSI_CODES["ORANGE_BG"] + ANSI_CODES["BLACK"] + ANSI_CODES["BOLD"],
        "title": ANSI_CODES["BOLD"],
        "example_title": ANSI_CODES["BOLD"],
        "example_input_string": ANSI_CODES["BOLD"],
        "example_output_string": ANSI_CODES["BOLD"],
        "example_explanation_string": ANSI_CODES["BOLD"],
        "example_input_data": ANSI_CODES["GRAY"],
        "example_output_data": ANSI_CODES["GRAY"],
        "example_explanation_data": ANSI_CODES["GRAY"],
        "constraints_string": ANSI_CODES["BOLD"],
        "Easy": ANSI_CODES["GREEN_BG"],
        "Medium": ANSI_CODES["ORANGE_BG"],
        "Hard": ANSI_CODES["RED_BG"],
    }

    HTML_TO_SYMBOL = {
        "sup": SYMBOLS["CARET"],
        "li": SYMBOLS["DOT"] + " ",
    }

    def __init__(self, problem):
        self.problem = problem

    @property
    def title(self) -> str:
        difficulty_color = self.HTML_TO_ANSI.get(self.problem.difficulty, "")
        title_text = f"[{self.problem.question_frontend_id}] {self.problem.title} {difficulty_color}[{self.problem.difficulty}]{ANSI_RESET}"
        return f"{self.HTML_TO_ANSI['title']}{title_text}{ANSI_RESET}"

    @property
    def description(self) -> str:
        if not self.problem.description:
            return "No description available."
        return self.html_to_ansi(self.problem.description)

    @property
    def examples(self) -> str:
        if not self.problem.examples:
            return "No examples available."
        formatted_examples = [self._format_example(ex) for ex in self.problem.examples]
        return "\n\n".join(formatted_examples)

    @property
    def constraints(self) -> str:
        if not self.problem.constraints:
            return ""
        # Each constraint is already an HTML string; convert each to ANSI
        constraints = [self.html_to_ansi(c) for c in self.problem.constraints]
        constraints_str = "\n".join(constraints)
        return f"{self.HTML_TO_ANSI['constraints_string']}Constraints:{ANSI_RESET}\n\n{constraints_str}"

    @property
    def topic_tags(self) -> str:
        if not self.problem.topic_tags:
            return ""
        formatted_tags = ["Tags:"]
        for tag in self.problem.topic_tags:
            tag_name = " " + tag.lower() + " "
            formatted_tags.append(self.HTML_TO_ANSI["tag"] + tag_name + ANSI_RESET + " ")
        return " ".join(formatted_tags)

    @property
    def languages(self) -> str:
        # code_snippets is a list of dicts with keys: code, lang, lang_slug
        langs = set(sn['lang'] for sn in self.problem.code_snippets if sn.get('lang'))
        if not langs:
            return "No code snippets available."
        formatted_languages = ["Languages:"]
        for language in langs:
            formatted_language = f"{self.HTML_TO_ANSI['language']} {language} {ANSI_RESET}"
            formatted_languages.append(formatted_language)
        return " ".join(formatted_languages)

    def html_to_ansi(self, html_content: str) -> str:
        """
        Converts HTML content to ANSI-formatted string.
        """
        if not html_content:
            return ""

        soup = BeautifulSoup(html_content, "html.parser")
        ansi_str = ""
        style_stack = []

        def traverse(element):
            nonlocal ansi_str
            if isinstance(element, NavigableString):
                ansi_str += element
            elif isinstance(element, Tag):
                if element.name in self.HTML_TO_SYMBOL:
                    ansi_str += self.HTML_TO_SYMBOL[element.name]
                if element.name in self.HTML_TO_ANSI:
                    ansi_code = self.HTML_TO_ANSI[element.name]
                    ansi_str += ansi_code
                    style_stack.append(ansi_code)
                # Insert line breaks after certain tags
                if element.name in ['p', 'br', 'ul']:
                    ansi_str += '\n'
                for child in element.children:
                    traverse(child)
                if element.name in self.HTML_TO_ANSI:
                    ansi_str += ANSI_RESET
                    if style_stack:
                        style_stack.pop()

        for child in soup.children:
            traverse(child)
        return ansi_str

    def _format_example(self, example: dict) -> str:
        """
        Formats a single example dictionary into a user-friendly string.
        example = {
            "title": "Example 1",
            "input": ["nums = [2,7,11,15]", "target = 9"],
            "output": "[0,1]",
            "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."
        }
        """
        parts = []
        # Title
        parts.append(f"{self.HTML_TO_ANSI['example_title']}{example.get('title', 'Example')}{ANSI_RESET}\n\n")

        # Input is a list of strings
        input_lines = example.get('input', [])
        input_str = ", ".join(input_lines)
        parts.append(f"| {self.HTML_TO_ANSI['example_input_string']}Input: {ANSI_RESET}{self.HTML_TO_ANSI['example_input_data']}{input_str}{ANSI_RESET}\n")

        # Output
        output_str = example.get('output', '')
        parts.append(f"| {self.HTML_TO_ANSI['example_output_string']}Output: {ANSI_RESET}{self.HTML_TO_ANSI['example_output_data']}{output_str}{ANSI_RESET}")

        # Explanation (if any)
        explanation = example.get('explanation', '')
        if explanation:
            explanation_formatted = explanation.replace("\n", f"{ANSI_RESET}\n| {self.HTML_TO_ANSI['example_explanation_data']}")
            parts.append(f"\n| {self.HTML_TO_ANSI['example_explanation_string']}Explanation: {ANSI_RESET}{self.HTML_TO_ANSI['example_explanation_data']}{explanation_formatted}{ANSI_RESET}")

        return "".join(parts)
