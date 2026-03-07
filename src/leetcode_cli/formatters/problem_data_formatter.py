import logging

from bs4 import BeautifulSoup, NavigableString, Tag

from leetcode_cli.exceptions.exceptions import ThemeError
from leetcode_cli.managers.theme_manager import ThemeManager
from leetcode_cli.models.problem import Problem

logger = logging.getLogger(__name__)


class ProblemFormatter:
    """
    Formats a single Problem object for terminal display using theme styling.
    """

    def __init__(self, problem: Problem, format_conf: dict, theme_manager: ThemeManager):
        self.problem = problem
        self.format_conf = format_conf
        self.theme_manager = theme_manager
        self.theme_data = theme_manager.load_theme_data()

        self.ANSI_RESET = "\033[0m"

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
            desc_str = self.description.rstrip("\xa0").lstrip("\n").rstrip("\n") or "No description available."
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

        spacing = self.theme_manager.get_layout_value("section_spacing", 2)
        separator = "\n" * (spacing + 1)
        return separator.join(sections)

    @property
    def title(self) -> str:
        difficulty = self.problem.difficulty
        title_ansi, _ = self.theme_manager.get_styling("text", "title")
        styled_title = f"{title_ansi}[{self.problem.question_frontend_id}] {self.problem.title}"

        diff_ansi, _ = self.theme_manager.get_styling("difficulty", difficulty.lower())

        return f"{styled_title}{self.ANSI_RESET} {diff_ansi}[{difficulty}]{self.ANSI_RESET}"

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

        heading_ansi, _ = self.theme_manager.get_styling("text", "heading")
        constraints_html = [self._html_to_ansi(c) for c in self.problem.constraints]
        combined = "\n".join(constraints_html)

        return f"{heading_ansi}Constraints:{self.ANSI_RESET}\n{combined}"

    @property
    def topic_tags(self) -> str:
        tags = self.problem.topic_tags
        if not tags:
            return ""

        heading_ansi, _ = self.theme_manager.get_styling("text", "heading")
        out = [f"{heading_ansi}tags:{self.ANSI_RESET}"]

        tag_ansi, _ = self.theme_manager.get_styling("text", "tag")
        for t in tags:
            out.append(f"{tag_ansi} {t.lower()} {self.ANSI_RESET}")

        return " ".join(out)

    @property
    def languages(self) -> str:
        langs = {sn["langSlug"] for sn in self.problem.code_snippets if sn.get("langSlug")}
        if not langs:
            return "No code snippets available."

        heading_ansi, _ = self.theme_manager.get_styling("text", "heading")
        lang_ansi, _ = self.theme_manager.get_styling("text", "language")

        out = [f"{heading_ansi}langs:{self.ANSI_RESET}"]
        for lang in sorted(langs):
            out.append(f"{lang_ansi} {lang} {self.ANSI_RESET}")

        return " ".join(out)

    def _html_to_ansi(self, html_content: str) -> str:
        if not html_content:
            return ""

        soup = BeautifulSoup(html_content, "html.parser")

        desc_ansi, _ = self.theme_manager.get_styling("text", "description")

        ansi_str = f"{desc_ansi}"
        style_stack = [("__base__", desc_ansi)]

        def traverse(el):
            nonlocal ansi_str, style_stack
            if isinstance(el, NavigableString):
                ansi_str += str(el)
            elif isinstance(el, Tag):
                if el.name == "sup":
                    ansi_str += "^"
                    for child in el.children:
                        traverse(child)
                    return

                elif el.name == "sub":
                    ansi_str += "_"
                    for child in el.children:
                        traverse(child)
                    return

                if el.name == "p" and el.get_text(strip=True) == "\xa0":
                    return

                try:
                    ansi_code, icon = self.theme_manager.get_styling("html", el.name.lower())
                except ThemeError:
                    ansi_code, icon = "", ""

                if icon:
                    ansi_str += icon

                if ansi_code:
                    ansi_str += ansi_code
                    style_stack.append((el.name, ansi_code))
                else:
                    style_stack.append((el.name, ""))

                for child in el.children:
                    traverse(child)

                style_stack.pop()

                ansi_str += self.ANSI_RESET
                for _, ansi in style_stack:
                    if ansi:
                        ansi_str += ansi

        for child in soup.children:
            traverse(child)

        ansi_str += self.ANSI_RESET

        return ansi_str

    def _format_example(self, example: dict) -> str:
        ex_title = example.get("title", "Example")

        label_ansi, _ = self.theme_manager.get_styling("text", "example_label")
        value_ansi, _ = self.theme_manager.get_styling("text", "example_value")

        lines = []
        lines.append(f"{label_ansi}{ex_title}{self.ANSI_RESET}\n")

        # Input
        raw_input = ", ".join(example.get("input", []))
        input_str = self._html_to_ansi(raw_input)

        input_line = f"{label_ansi}| Input: {self.ANSI_RESET}"
        input_line += f"{value_ansi}{input_str}{self.ANSI_RESET}".replace(
            "\n",
            self.ANSI_RESET + "\n" + f"{label_ansi}| " + " " * 7 + f"{self.ANSI_RESET}{value_ansi}",
        )
        lines.append(input_line + "\n")

        # Output
        raw_output = example.get("output", "")
        out_str = self._html_to_ansi(raw_output)

        output_line = f"{label_ansi}| Output: {self.ANSI_RESET}"
        output_line += f"{value_ansi}{out_str}{self.ANSI_RESET}".replace(
            "\n",
            self.ANSI_RESET + "\n" + f"{label_ansi}| " + " " * 8 + f"{self.ANSI_RESET}{value_ansi}",
        )
        lines.append(output_line + "\n")

        # Explanation
        explanation = example.get("explanation", "")
        if explanation:
            expl_str = self._html_to_ansi(explanation)

            explanation_line = f"{label_ansi}| Explanation: {self.ANSI_RESET}"
            explanation_line += f"{value_ansi}{expl_str}{self.ANSI_RESET}".replace(
                "\n",
                self.ANSI_RESET + "\n" + f"{label_ansi}| " + " " * 13 + f"{self.ANSI_RESET}{value_ansi}",
            )
            lines.append(explanation_line + "\n")

        return "".join(lines)
