from bs4 import BeautifulSoup, NavigableString, Tag

from leetcode_cli.utils.theme_utils import load_theme_data
from leetcode_cli.graphics.ansi_codes import ANSI_RESET
from leetcode_cli.exceptions.exceptions import ThemeError
from leetcode_cli.models.problem import Problem

class ProblemFormatter:
    def __init__(self, problem: Problem, format_conf: dict):
        self.problem = problem
        self.format_conf = format_conf

        try:
            self.theme_data = load_theme_data()

        except ThemeError as e:
            raise ThemeError(f"Failed to load theme: {e}")

    def get_formatted_problem(self) -> str:
        sections = []

        if self.format_conf.get("show_title", True):
            title_str = self.title
            if title_str:
                sections.append(title_str)

        if self.format_conf.get("show_tags", True):
            tags_str = self.topic_tags
            if tags_str:
                sections.append(tags_str)

        if self.format_conf.get("show_langs", True):
            langs_str = self.languages
            sections.append(langs_str)

        if self.format_conf.get("show_description", True):
            desc_str = self.description.lstrip("\n") or "No description available."
            sections.append(desc_str)

        if self.format_conf.get("show_examples", True):
            ex_str = self.examples
            if ex_str.strip():
                sections.append(ex_str)
            else:
                sections.append("No examples available.")

        if self.format_conf.get("show_constraints", True):
            con_str = self.constraints
            if con_str.strip():
                sections.append(con_str)

        return "\n\n".join(sections)

    @property
    def title(self) -> str:
        difficulty_color = self.theme_data['PROBLEM_FORMATTER_ANSI_CODES'].get(self.problem.difficulty, "")
        title_text = f"[{self.problem.question_frontend_id}] {self.problem.title} " \
                     f"{difficulty_color}[{self.problem.difficulty}]{ANSI_RESET}"

        return f"{self.theme_data['PROBLEM_FORMATTER_ANSI_CODES']['title']}{title_text}{ANSI_RESET}"

    @property
    def description(self) -> str:
        if not self.problem.description:
            return ""

        return self.html_to_ansi(self.problem.description)

    @property
    def examples(self) -> str:
        if not self.problem.examples:
            return ""

        formatted_examples = [self._format_example(ex) for ex in self.problem.examples]

        return "\n\n".join(formatted_examples)

    @property
    def constraints(self) -> str:
        if not self.problem.constraints:
            return ""

        constraints_ansi = [self.html_to_ansi(c) for c in self.problem.constraints]
        constraints_str = "\n".join(constraints_ansi)

        return (
            f"{self.theme_data['PROBLEM_FORMATTER_ANSI_CODES']['constraints_string']}Constraints:{ANSI_RESET}\n\n"
            f"{constraints_str}"
        )

    @property
    def topic_tags(self) -> str:
        if not self.problem.topic_tags:
            return ""

        formatted_tags = ["Tags:"]
        for tag in self.problem.topic_tags:
            tag_name = " " + tag.lower() + " "
            formatted_tags.append(
                self.theme_data['PROBLEM_FORMATTER_ANSI_CODES']["tag"]
                + tag_name
                + ANSI_RESET
                + " "
            )

        return " ".join(formatted_tags)

    @property
    def languages(self) -> str:
        langs = {sn['lang'] for sn in self.problem.code_snippets if sn.get('lang')}
        if not langs:
            return "No code snippets available."

        formatted_languages = ["Languages:"]
        for language in sorted(langs):
            formatted_languages.append(
                f"{self.theme_data['PROBLEM_FORMATTER_ANSI_CODES']['language']} {language} {ANSI_RESET}"
            )
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
                # If we have a symbol mapping for this element (like <li>, <sup>, etc.)
                if element.name in self.theme_data['PROBLEM_FORMATTER_SYMBOLS']:
                    ansi_str += self.theme_data['PROBLEM_FORMATTER_SYMBOLS'][element.name]

                # If we have an ANSI code for this element (like <strong>, <b>, etc.)
                if element.name in self.theme_data['PROBLEM_FORMATTER_ANSI_CODES']:
                    ansi_code = self.theme_data['PROBLEM_FORMATTER_ANSI_CODES'][element.name]
                    ansi_str += ansi_code
                    style_stack.append(ansi_code)

                # Insert a newline for block elements
                if element.name in ['p', 'br', 'ul']:
                    ansi_str += '\n'

                for child in element.children:
                    traverse(child)

                # Pop styling if we applied something
                if element.name in self.theme_data['PROBLEM_FORMATTER_ANSI_CODES']:
                    ansi_str += ANSI_RESET
                    if style_stack:
                        style_stack.pop()

        for child in soup.children:
            traverse(child)

        return ansi_str

    def _format_example(self, example: dict) -> str:
        parts = []

        parts.append(
            f"{self.theme_data['PROBLEM_FORMATTER_ANSI_CODES']['example_title']}"
            f"{example.get('title', 'Example')}{ANSI_RESET}\n\n"
        )

        input_lines = example.get('input', [])
        input_str = ", ".join(input_lines)

        parts.append(
            f"| {self.theme_data['PROBLEM_FORMATTER_ANSI_CODES']['example_input_string']}Input: {ANSI_RESET}"
            f"{self.theme_data['PROBLEM_FORMATTER_ANSI_CODES']['example_input_data']}{input_str}{ANSI_RESET}\n"
        )

        output_str = example.get('output', '')
        parts.append(
            f"| {self.theme_data['PROBLEM_FORMATTER_ANSI_CODES']['example_output_string']}Output: {ANSI_RESET}"
            f"{self.theme_data['PROBLEM_FORMATTER_ANSI_CODES']['example_output_data']}{output_str}{ANSI_RESET}"
        )

        explanation = example.get('explanation', '')

        if explanation:
            explanation_formatted = explanation.replace(
                "\n",
                f"{ANSI_RESET}\n| {self.theme_data['PROBLEM_FORMATTER_ANSI_CODES']['example_explanation_data']}"
            )

            parts.append(
                f"\n| {self.theme_data['PROBLEM_FORMATTER_ANSI_CODES']['example_explanation_string']}Explanation: {ANSI_RESET}"
                f"{self.theme_data['PROBLEM_FORMATTER_ANSI_CODES']['example_explanation_data']}"
                f"{explanation_formatted}{ANSI_RESET}"
            )

        return "".join(parts)
