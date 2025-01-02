import logging

from bs4 import BeautifulSoup, NavigableString, Tag
from leetcode_cli.graphics.ansi_codes import ANSI_RESET
from leetcode_cli.models.problem import Problem
from leetcode_cli.models.theme import ThemeData
from leetcode_cli.services.theme_service import get_styling
from leetcode_cli.exceptions.exceptions import ThemeError

logger = logging.getLogger(__name__)

class ProblemFormatter:
    """
    Formats a single Problem object, referencing MAPPINGS['PROBLEM_DESCRIPTION'] for tags, difficulties, etc.
    """
    def __init__(self, problem: Problem, format_conf: dict, theme_data: ThemeData):
        self.problem = problem
        self.format_conf = format_conf
        self.theme_data = theme_data

    def get_formatted_problem(self) -> str:
        sections = []

        if self.format_conf.get("show_title", True):
            sections.append(self.title or "")

        if self.format_conf.get("show_tags", True):
            tags_str = self.topic_tags
            if tags_str:
                sections.append(tags_str)

        if self.format_conf.get("show_langs", True):
            sections.append(self.languages)

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
        difficulty = self.problem.difficulty
        try:
            diff_ansi, diff_symbol = get_styling(self.theme_data, "PROBLEM_DESCRIPTION", difficulty)
            title_ansi, title_symbol = get_styling(self.theme_data, "PROBLEM_DESCRIPTION", "title")

        except ThemeError as te:
            logger.error(f"Theming Error: {te}")
            raise te

        text = f"[{self.problem.question_frontend_id}] {self.problem.title} {diff_ansi}{difficulty}{ANSI_RESET}"
        return f"{title_ansi}{title_symbol}{text}{ANSI_RESET}"

    @property
    def description(self) -> str:
        if not self.problem.description:
            return ""
        return self._html_to_ansi(self.problem.description)

    @property
    def examples(self) -> str:
        if not self.problem.examples:
            return ""
        return "\n\n".join(self._format_example(ex) for ex in self.problem.examples)

    @property
    def constraints(self) -> str:
        if not self.problem.constraints:
            return ""
        try:
            constraints_ansi, symbol = get_styling(self.theme_data, "PROBLEM_DESCRIPTION", "constraints_string")
        except ThemeError as te:
            logger.error(f"Theming Error: {te}")
            raise te
        constraints_html = [self._html_to_ansi(c) for c in self.problem.constraints]
        combined = "\n".join(constraints_html)
        return f"{constraints_ansi}{symbol}Constraints:{ANSI_RESET}\n\n{combined}"

    @property
    def topic_tags(self) -> str:
        tags = self.problem.topic_tags
        if not tags:
            return ""
        try:
            label_ansi, symbol = get_styling(self.theme_data, "PROBLEM_DESCRIPTION", "tag_label")
        except ThemeError as te:
            logger.error(f"Theming Error: {te}")
            raise te
        out = [f"{label_ansi}{symbol}Tags:{ANSI_RESET}"]
        for t in tags:
            try:
                tag_ansi, tag_symbol = get_styling(self.theme_data, "PROBLEM_DESCRIPTION", "tag")
            except ThemeError as te:
                logger.error(f"Theming Error: {te}")
                raise te
            out.append(f"{tag_ansi}{tag_symbol}{t.lower()}{tag_symbol}{ANSI_RESET}")
        return " ".join(out)

    @property
    def languages(self) -> str:
        langs = {sn['lang'] for sn in self.problem.code_snippets if sn.get('lang')}
        if not langs:
            return "No code snippets available."

        try:
            label_ansi, symbol = get_styling(self.theme_data, "PROBLEM_DESCRIPTION", "language_label")
            lang_ansi, lang_symbol = get_styling(self.theme_data, "PROBLEM_DESCRIPTION", "language")
        except ThemeError as te:
            logger.error(f"Theming Error: {te}")
            raise te
        out = [f"{label_ansi}{symbol}Languages:{ANSI_RESET}"]
        for lang in sorted(langs):
            out.append(f"{lang_ansi}{lang_symbol}{lang}{lang_symbol}{ANSI_RESET}")
        return " ".join(out)

    def _html_to_ansi(self, html_content: str) -> str:
        if not html_content:
            return ""
        soup = BeautifulSoup(html_content, "html.parser")
        ansi_str = ""

        def traverse(el):
            nonlocal ansi_str
            if isinstance(el, NavigableString):
                ansi_str += el
            elif isinstance(el, Tag):
                # Get styling for this tag
                try:
                    ansi_code, symbol = get_styling(self.theme_data, "PROBLEM_DESCRIPTION", el.name)
                except ThemeError as te:
                    logger.error(f"Theming Error: {te}")
                    raise te

                ansi_str += f"{ansi_code}{symbol}"

                if el.name in ["p", "br", "ul", "ol"]:
                    ansi_str += "\n"

                for child in el.children:
                    traverse(child)

                ansi_str += ANSI_RESET

        for child in soup.children:
            traverse(child)
        return ansi_str

    def _format_example(self, example: dict) -> str:
        ex_title = example.get('title', 'Example')

        try:
            ex_title_ansi, symbol = get_styling(self.theme_data, "PROBLEM_DESCRIPTION", "example_title")
        except ThemeError as te:
            logger.error(f"Theming Error: {te}")
            raise te
        lines = []
        lines.append(f"{ex_title_ansi}{symbol}{ex_title}{ANSI_RESET}\n")

        # Input
        input_str = ", ".join(example.get('input', []))
        try:
            ex_input_str_ansi, symbol_input = get_styling(self.theme_data, "PROBLEM_DESCRIPTION", "example_input_string")
            ex_input_data_ansi, symbol_input_data = get_styling(self.theme_data, "PROBLEM_DESCRIPTION", "example_input_data")
        except ThemeError as te:
            logger.error(f"Theming Error: {te}")
            raise te
        lines.append(f"| {ex_input_str_ansi}{symbol_input}Input:{ANSI_RESET} {ex_input_data_ansi}{symbol_input_data}{input_str}{ANSI_RESET}\n")

        # Output
        out_str = example.get('output', "")
        try:
            ex_output_str_ansi, symbol_output = get_styling(self.theme_data, "PROBLEM_DESCRIPTION", "example_output_string")
            ex_output_data_ansi, symbol_output_data = get_styling(self.theme_data, "PROBLEM_DESCRIPTION", "example_output_data")
        except ThemeError as te:
            logger.error(f"Theming Error: {te}")
            raise te
        lines.append(f"| {ex_output_str_ansi}{symbol_output}Output:{ANSI_RESET} {ex_output_data_ansi}{symbol_output_data}{out_str}{ANSI_RESET}")

        # Explanation
        explanation = example.get('explanation', "")
        if explanation:
            try:
                ex_expl_str_ansi, symbol_expl = get_styling(self.theme_data, "PROBLEM_DESCRIPTION", "example_explanation_string")
                ex_expl_data_ansi, symbol_expl_data = get_styling(self.theme_data, "PROBLEM_DESCRIPTION", "example_explanation_data")
            except ThemeError as te:
                logger.error(f"Theming Error: {te}")
                raise te
            replaced = explanation.replace('\n', f'{ANSI_RESET}\n| {ex_expl_data_ansi}{symbol_expl_data}')
            lines.append(
                f"\n| {ex_expl_str_ansi}{symbol_expl}Explanation:{ANSI_RESET} "
                f"{ex_expl_data_ansi}{symbol_expl_data}{replaced}{ANSI_RESET}"
            )
        return "".join(lines)
