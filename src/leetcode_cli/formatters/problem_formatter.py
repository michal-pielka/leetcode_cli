from bs4 import BeautifulSoup, NavigableString, Tag

from leetcode_cli.graphics.ansi_codes import ANSI_RESET
from leetcode_cli.models.problem import Problem
from leetcode_cli.models.theme import ThemeData
from leetcode_cli.services.theme_service import get_ansi_code, get_symbol

class ProblemFormatter:
    def __init__(self, problem: Problem, format_conf: dict, theme_data: ThemeData):
        self.problem = problem
        self.format_conf = format_conf
        self.theme_data = theme_data

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
        difficulty_color = get_ansi_code(self.theme_data, 'PROBLEM_FORMATTER_ANSI_CODES', self.problem.difficulty)
        title_style = get_ansi_code(self.theme_data, 'PROBLEM_FORMATTER_ANSI_CODES', 'title')

        text = f"[{self.problem.question_frontend_id}] {self.problem.title} {difficulty_color}[{self.problem.difficulty}]{ANSI_RESET}"
        return f"{title_style}{text}{ANSI_RESET}"

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
        constraints_string_code = get_ansi_code(self.theme_data, 'PROBLEM_FORMATTER_ANSI_CODES', 'constraints_string')
        constraints_str = "\n".join(constraints_ansi)

        return f"{constraints_string_code}Constraints:{ANSI_RESET}\n\n{constraints_str}"

    @property
    def topic_tags(self) -> str:
        if not self.problem.topic_tags:
            return ""
        formatted_tags = ["Tags:"]
        for tag in self.problem.topic_tags:
            tag_name = " " + tag.lower() + " "
            tag_code = get_ansi_code(self.theme_data, 'PROBLEM_FORMATTER_ANSI_CODES', 'tag')
            formatted_tags.append(f"{tag_code}{tag_name}{ANSI_RESET} ")
        return " ".join(formatted_tags)

    @property
    def languages(self) -> str:
        langs = {sn['lang'] for sn in self.problem.code_snippets if sn.get('lang')}
        if not langs:
            return "No code snippets available."

        formatted_languages = ["Languages:"]
        for language in sorted(langs):
            language_code = get_ansi_code(self.theme_data, 'PROBLEM_FORMATTER_ANSI_CODES', 'language')
            formatted_languages.append(f"{language_code} {language} {ANSI_RESET}")
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
                if element.name:
                    # Attempt symbol
                    sym = get_symbol(self.theme_data, 'PROBLEM_FORMATTER_SYMBOLS', element.name)
                    ansi_str += sym

                if element.name:
                    ansi_code = get_ansi_code(self.theme_data, 'PROBLEM_FORMATTER_ANSI_CODES', element.name)
                    ansi_str += ansi_code
                    style_stack.append(ansi_code)

                # Insert a newline for certain block elements
                if element.name in ['p', 'br', 'ul']:
                    ansi_str += '\n'

                for child in element.children:
                    traverse(child)

                if element.name:
                    _ = get_ansi_code(self.theme_data, 'PROBLEM_FORMATTER_ANSI_CODES', element.name)  
                    ansi_str += ANSI_RESET
                    if style_stack:
                        style_stack.pop()

        for child in soup.children:
            traverse(child)

        return ansi_str

    def _format_example(self, example: dict) -> str:
        # --------------- REMOVE fallback logic; just let ThemeError bubble up ---------------
        example_title_code = get_ansi_code(self.theme_data, 'PROBLEM_FORMATTER_ANSI_CODES', 'example_title')
        example_input_string_code = get_ansi_code(self.theme_data, 'PROBLEM_FORMATTER_ANSI_CODES', 'example_input_string')
        example_input_data_code = get_ansi_code(self.theme_data, 'PROBLEM_FORMATTER_ANSI_CODES', 'example_input_data')
        example_output_string_code = get_ansi_code(self.theme_data, 'PROBLEM_FORMATTER_ANSI_CODES', 'example_output_string')
        example_output_data_code = get_ansi_code(self.theme_data, 'PROBLEM_FORMATTER_ANSI_CODES', 'example_output_data')
        example_explanation_string_code = get_ansi_code(self.theme_data, 'PROBLEM_FORMATTER_ANSI_CODES', 'example_explanation_string')
        example_explanation_data_code = get_ansi_code(self.theme_data, 'PROBLEM_FORMATTER_ANSI_CODES', 'example_explanation_data')
        # ------------------------------------------------------------------------------------

        parts = []
        parts.append(f"{example_title_code}{example.get('title', 'Example')}{ANSI_RESET}\n\n")
        input_lines = example.get('input', [])
        input_str = ", ".join(input_lines)

        parts.append(
            f"| {example_input_string_code}Input: {ANSI_RESET}"
            f"{example_input_data_code}{input_str}{ANSI_RESET}\n"
        )

        output_str = example.get('output', '')
        parts.append(
            f"| {example_output_string_code}Output: {ANSI_RESET}"
            f"{example_output_data_code}{output_str}{ANSI_RESET}"
        )

        explanation = example.get('explanation', '')
        if explanation:
            explanation_formatted = explanation.replace(
                "\n",
                f"{ANSI_RESET}\n| {example_explanation_data_code}"
            )
            parts.append(
                f"\n| {example_explanation_string_code}Explanation: {ANSI_RESET}"
                f"{example_explanation_data_code}{explanation_formatted}{ANSI_RESET}"
            )
        return "".join(parts)
