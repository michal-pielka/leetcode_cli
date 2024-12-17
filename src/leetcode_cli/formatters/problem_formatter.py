from bs4 import BeautifulSoup, NavigableString, Tag
from leetcode_cli.utils.theme_utils import get_theme_data
from leetcode_cli.graphics.ansi_codes import ANSI_RESET

class ProblemFormatter:
    def __init__(self, problem):
        self.problem = problem
        self.THEME_DATA = get_theme_data()

    @property
    def title(self) -> str:
        difficulty_color = self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES'].get(self.problem.difficulty, "")
        title_text = f"[{self.problem.question_frontend_id}] {self.problem.title} {difficulty_color}[{self.problem.difficulty}]{ANSI_RESET}"
        return f"{self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']['title']}{title_text}{ANSI_RESET}"

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
        constraints = [self.html_to_ansi(c) for c in self.problem.constraints]
        constraints_str = "\n".join(constraints)
        return f"{self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']['constraints_string']}Constraints:{ANSI_RESET}\n\n{constraints_str}"

    @property
    def topic_tags(self) -> str:
        if not self.problem.topic_tags:
            return ""
        formatted_tags = ["Tags:"]
        for tag in self.problem.topic_tags:
            tag_name = " " + tag.lower() + " "
            formatted_tags.append(self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']["tag"] + tag_name + ANSI_RESET + " ")
        return " ".join(formatted_tags)

    @property
    def languages(self) -> str:
        langs = set(sn['lang'] for sn in self.problem.code_snippets if sn.get('lang'))
        if not langs:
            return "No code snippets available."
        formatted_languages = ["Languages:"]
        for language in langs:
            formatted_language = f"{self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']['language']} {language} {ANSI_RESET}"
            formatted_languages.append(formatted_language)
        return " ".join(formatted_languages)

    def html_to_ansi(self, html_content: str) -> str:
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
                if element.name in self.THEME_DATA['PROBLEM_FORMATTER_SYMBOLS']:
                    ansi_str += self.THEME_DATA['PROBLEM_FORMATTER_SYMBOLS'][element.name]
                if element.name in self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']:
                    ansi_code = self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES'][element.name]
                    ansi_str += ansi_code
                    style_stack.append(ansi_code)
                if element.name in ['p', 'br', 'ul']:
                    ansi_str += '\n'
                for child in element.children:
                    traverse(child)
                if element.name in self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']:
                    ansi_str += ANSI_RESET
                    if style_stack:
                        style_stack.pop()

        for child in soup.children:
            traverse(child)
        return ansi_str

    def _format_example(self, example: dict) -> str:
        parts = []
        parts.append(f"{self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']['example_title']}{example.get('title', 'Example')}{ANSI_RESET}\n\n")
        input_lines = example.get('input', [])
        input_str = ", ".join(input_lines)
        parts.append(f"| {self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']['example_input_string']}Input: {ANSI_RESET}{self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']['example_input_data']}{input_str}{ANSI_RESET}\n")
        output_str = example.get('output', '')
        parts.append(f"| {self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']['example_output_string']}Output: {ANSI_RESET}{self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']['example_output_data']}{output_str}{ANSI_RESET}")
        explanation = example.get('explanation', '')
        if explanation:
            explanation_formatted = explanation.replace("\n", f"{ANSI_RESET}\n| {self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']['example_explanation_data']}")
            parts.append(f"\n| {self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']['example_explanation_string']}Explanation: {ANSI_RESET}{self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']['example_explanation_data']}{explanation_formatted}{ANSI_RESET}")

        return "".join(parts)
