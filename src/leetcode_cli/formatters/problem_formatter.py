from bs4 import BeautifulSoup, NavigableString, Tag

from leetcode_cli.utils.theme_utils import load_problem_theme_data
from leetcode_cli.graphics.ansi_codes import ANSI_RESET
from leetcode_cli.exceptions.exceptions import ThemeError

class ProblemFormatter:
    def __init__(self, problem, format_conf: dict):
        self.problem = problem
        self.format_conf = format_conf

        try:
            self.THEME_DATA = load_problem_theme_data()

        except ThemeError as e:
            raise ThemeError(f"Failed to load theme: {str(e)}")

    def get_formatted_problem(self) -> str:
        sections = []

        # Title
        if self.format_conf.get("show_title", True):
            # Use the property-based approach
            title_str = self.title
            if title_str:
                sections.append(title_str)

        # Tags
        if self.format_conf.get("show_tags", True):
            tags_str = self.topic_tags
            # Could be empty if no tags
            if tags_str:
                sections.append(tags_str)

        # Languages
        if self.format_conf.get("show_langs", True):
            langs_str = self.languages
            sections.append(langs_str)

        # Description
        if self.format_conf.get("show_description", True):
            desc_str = self.description or "No description available."
            sections.append(desc_str)

        # Examples
        if self.format_conf.get("show_examples", True):
            ex_str = self.examples
            if ex_str.strip():
                sections.append(ex_str)

            else:
                sections.append("No examples available.")

        # Constraints
        if self.format_conf.get("show_constraints", True):
            con_str = self.constraints
            if con_str.strip():
                sections.append(con_str)

        # Join with double newlines
        return "\n\n".join(sections)

    @property
    def title(self) -> str:
        difficulty_color = self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES'].get(self.problem.difficulty, "")
        title_text = f"[{self.problem.question_frontend_id}] {self.problem.title} " \
                     f"{difficulty_color}[{self.problem.difficulty}]{ANSI_RESET}"

        return f"{self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']['title']}{title_text}{ANSI_RESET}"

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
            f"{self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']['constraints_string']}Constraints:{ANSI_RESET}\n\n"
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
                self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']["tag"]
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
                f"{self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']['language']} {language} {ANSI_RESET}"
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
                # If we have a symbol mapping for this element
                if element.name in self.THEME_DATA['PROBLEM_FORMATTER_SYMBOLS']:
                    ansi_str += self.THEME_DATA['PROBLEM_FORMATTER_SYMBOLS'][element.name]

                # If we have an ANSI code for this element (like <strong>, <b>, etc.)
                if element.name in self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']:
                    ansi_code = self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES'][element.name]
                    ansi_str += ansi_code
                    style_stack.append(ansi_code)

                # Insert a newline for certain block elements
                if element.name in ['p', 'br', 'ul']:
                    ansi_str += '\n'

                # Recurse children
                for child in element.children:
                    traverse(child)

                # Pop styling if we applied something
                if element.name in self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']:
                    ansi_str += ANSI_RESET
                    if style_stack:
                        style_stack.pop()

        for child in soup.children:
            traverse(child)

        return ansi_str

    def _parse_example_content(self, html_content: str, title: str) -> dict:
        """
        Used internally if you want to parse <pre> blocks into
        input/output/explanation fields. (Your code remains as is.)
        """
        import re
        soup = BeautifulSoup(html_content, "html.parser")
        content_text = soup.get_text(separator="\n").strip()
        example_dict = {"title": title}

        input_match = re.search(r'Input:\s*(.*?)(?:\nOutput:|\Z)', content_text, re.DOTALL)
        output_match = re.search(r'Output:\s*(.*?)(?:\nExplanation:|\Z)', content_text, re.DOTALL)
        explanation_match = re.search(r'Explanation:\s*(.*)', content_text, re.DOTALL)

        input_str = input_match.group(1).strip() if input_match else ""
        input_list = []
        if input_str:
            parts = [part.strip() for part in input_str.split(',')]
            input_list = [p for p in parts if p]

        example_dict['input'] = input_list
        example_dict['output'] = output_match.group(1).strip() if output_match else ""
        example_dict['explanation'] = explanation_match.group(1).strip() if explanation_match else ""

        return example_dict

    def _parse_example_section(self, header):
        """
        If you want to parse an HTML header to find the next <pre> block, etc.
        """
        example_title = header.get_text(strip=True).rstrip(':')
        pre_tag = header.find_next('pre')
        if not pre_tag:
            return None
        example_content = pre_tag.decode_contents()
        return self._parse_example_content(example_content, example_title)

    def _format_example(self, example: dict) -> str:
        """
        Takes a dict like {"title": ..., "input": [...], "output": ..., "explanation": ...}
        and returns an ANSI-formatted string using your theme data.
        """
        parts = []
        # Title
        parts.append(
            f"{self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']['example_title']}"
            f"{example.get('title', 'Example')}{ANSI_RESET}\n\n"
        )

        # Input
        input_lines = example.get('input', [])
        input_str = ", ".join(input_lines)
        parts.append(
            f"| {self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']['example_input_string']}Input: {ANSI_RESET}"
            f"{self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']['example_input_data']}"
            f"{input_str}{ANSI_RESET}\n"
        )

        # Output
        output_str = example.get('output', '')
        parts.append(
            f"| {self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']['example_output_string']}Output: {ANSI_RESET}"
            f"{self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']['example_output_data']}"
            f"{output_str}{ANSI_RESET}"
        )

        # Explanation
        explanation = example.get('explanation', '')
        if explanation:
            explanation_formatted = explanation.replace(
                "\n", f"{ANSI_RESET}\n| {self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']['example_explanation_data']}"
            )
            parts.append(
                f"\n| {self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']['example_explanation_string']}Explanation: {ANSI_RESET}"
                f"{self.THEME_DATA['PROBLEM_FORMATTER_ANSI_CODES']['example_explanation_data']}"
                f"{explanation_formatted}{ANSI_RESET}"
            )

        return "".join(parts)
