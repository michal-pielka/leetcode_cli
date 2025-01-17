import logging

from bs4 import BeautifulSoup, NavigableString, Tag
from leetcode_cli.models.problem import Problem
from leetcode_cli.managers.theme_manager import ThemeManager
from leetcode_cli.exceptions.exceptions import ThemeError

logger = logging.getLogger(__name__)


class ProblemFormatter:
    """
    Formats a single Problem object, referencing MAPPINGS['PROBLEM_DESCRIPTION'] for tags, difficulties, etc.
    """

    def __init__(
        self, problem: Problem, format_conf: dict, theme_manager: ThemeManager
    ):
        self.problem = problem
        self.format_conf = format_conf
        self.theme_manager = theme_manager
        self.theme_data = theme_manager.load_theme_data()

        self.ANSI_RESET = "\033[0m"  # Reset all styles

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
            desc_str = (
                self.description.rstrip("\xa0").lstrip("\n").rstrip("\n")
                or "No description available."
            )
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

        return "\n\n\n".join(sections)

    @property
    def title(self) -> str:
        difficulty = self.problem.difficulty
        try:
            # Styling for title
            title_ansi, title_symbol_left, title_symbol_right = (
                self.theme_manager.get_styling("PROBLEM_DESCRIPTION", "label_title")
            )
            styled_title = f"{title_ansi}{title_symbol_left}[{self.problem.question_frontend_id}] {self.problem.title}{title_symbol_right}"
            diff_ansi, diff_symbol_left, diff_symbol_right = (
                self.theme_manager.get_styling(
                    "PROBLEM_DESCRIPTION", "difficulty_" + difficulty.lower()
                )
            )

        except ThemeError as te:
            logger.error(f"Theming Error: {te}")
            raise te

        return f"{styled_title}{self.ANSI_RESET} {diff_ansi}{diff_symbol_left}{difficulty}{diff_symbol_right}{self.ANSI_RESET}"

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
            constraints_ansi, constraints_symbol_left, constraints_symbol_right = (
                self.theme_manager.get_styling(
                    "PROBLEM_DESCRIPTION", "label_constraints"
                )
            )

        except ThemeError as te:
            logger.error(f"Theming Error: {te}")
            raise te

        constraints_html = [self._html_to_ansi(c) for c in self.problem.constraints]
        combined = "\n".join(constraints_html)

        return f"{constraints_ansi}{constraints_symbol_left}Constraints:{constraints_symbol_right}{self.ANSI_RESET}\n{combined}"

    @property
    def topic_tags(self) -> str:
        tags = self.problem.topic_tags
        if not tags:
            return ""
        try:
            label_ansi, label_symbol_left, label_symbol_right = (
                self.theme_manager.get_styling("PROBLEM_DESCRIPTION", "label_tags")
            )

        except ThemeError as te:
            logger.error(f"Theming Error: {te}")
            raise te

        out = [
            f"{label_ansi}{label_symbol_left}tags:{label_symbol_right}{self.ANSI_RESET}"
        ]
        for t in tags:
            try:
                tag_ansi, tag_symbol_left, tag_symbol_right = (
                    self.theme_manager.get_styling("PROBLEM_DESCRIPTION", "value_tags")
                )

            except ThemeError as te:
                logger.error(f"Theming Error: {te}")
                raise te

            out.append(
                f"{tag_ansi}{tag_symbol_left}{t.lower()}{tag_symbol_right}{self.ANSI_RESET}"
            )

        return " ".join(out)

    @property
    def languages(self) -> str:
        langs = {
            sn["langSlug"] for sn in self.problem.code_snippets if sn.get("langSlug")
        }
        if not langs:
            return "No code snippets available."

        try:
            label_ansi, label_symbol_left, label_symbol_right = (
                self.theme_manager.get_styling("PROBLEM_DESCRIPTION", "label_languages")
            )
            lang_ansi, lang_symbol_left, lang_symbol_right = (
                self.theme_manager.get_styling("PROBLEM_DESCRIPTION", "value_languages")
            )

        except ThemeError as te:
            logger.error(f"Theming Error: {te}")
            raise te

        out = [
            f"{label_ansi}{label_symbol_left}langs:{label_symbol_right}{self.ANSI_RESET}"
        ]
        for lang in sorted(langs):
            out.append(
                f"{lang_ansi}{lang_symbol_left}{lang}{lang_symbol_right}{self.ANSI_RESET}"
            )

        return " ".join(out)

    def _html_to_ansi(self, html_content: str) -> str:
        if not html_content:
            return ""

        soup = BeautifulSoup(html_content, "html.parser")
        ansi_str = ""
        style_stack = []

        def traverse(el):
            nonlocal ansi_str, style_stack
            if isinstance(el, NavigableString):
                ansi_str += el
            elif isinstance(el, Tag):
                # Handle <sup> tags by prefixing with caret (^)
                if el.name == "sup":
                    ansi_str += "^"
                    # Traverse the children without any additional styling
                    for child in el.children:
                        traverse(child)
                    return  # Skip further processing

                # Handle <sub> tags by prefixing with underscore (_)
                elif el.name == "sub":
                    ansi_str += "_"
                    # Traverse the children without any additional styling
                    for child in el.children:
                        traverse(child)
                    return  # Skip further processing

                # Handle empty <p> tags containing only non-breaking spaces
                if el.name == "p" and el.get_text(strip=True) == "\xa0":
                    return  # Skip adding anything for this tag

                # Get the styling for the current tag
                try:
                    ansi_code, symbol_left, symbol_right = (
                        self.theme_manager.get_styling(
                            "PROBLEM_DESCRIPTION", "html_" + el.name.lower()
                        )
                    )

                except ThemeError as te:
                    raise te

                # Apply the current tag's ANSI code and symbols
                if ansi_code:
                    ansi_str += f"{ansi_code}{symbol_left}"
                    style_stack.append((el.name, ansi_code))

                else:
                    style_stack.append((el.name, ""))

                # Traverse child elements
                for child in el.children:
                    traverse(child)

                # Close the current tag's styling
                if symbol_right:
                    ansi_str += f"{symbol_right}"

                # Pop the current tag from the stack
                popped_tag, popped_ansi = style_stack.pop()

                # Determine if an ANSI reset is needed
                if popped_tag in ["code", "pre"]:
                    ansi_str += self.ANSI_RESET
                    # Re-apply remaining styles
                    for tag, ansi in style_stack:
                        if ansi:
                            ansi_str += ansi
                else:
                    # Re-apply remaining styles by resetting and re-applying
                    if popped_ansi:
                        ansi_str += self.ANSI_RESET
                        for tag, ansi in style_stack:
                            if ansi:
                                ansi_str += ansi

        for child in soup.children:
            traverse(child)

        return ansi_str

    def _format_example(self, example: dict) -> str:
        ex_title = example.get("title", "Example")

        try:
            ex_title_ansi, ex_title_symbol_left, ex_title_symbol_right = (
                self.theme_manager.get_styling(
                    "PROBLEM_DESCRIPTION", "label_example_title"
                )
            )

        except ThemeError as te:
            logger.error(f"Theming Error: {te}")
            raise te

        lines = []
        lines.append(
            f"{ex_title_ansi}{ex_title_symbol_left}{ex_title}{ex_title_symbol_right}{self.ANSI_RESET}\n"
        )

        # Input
        raw_input = ", ".join(example.get("input", []))
        input_str = self._html_to_ansi(raw_input)
        try:
            ex_input_str_ansi, ex_input_symbol_left, ex_input_symbol_right = (
                self.theme_manager.get_styling(
                    "PROBLEM_DESCRIPTION", "label_example_input"
                )
            )
            (
                ex_input_data_ansi,
                ex_input_data_symbol_left,
                ex_input_data_symbol_right,
            ) = self.theme_manager.get_styling(
                "PROBLEM_DESCRIPTION", "value_example_input"
            )

        except ThemeError as te:
            logger.error(f"Theming Error: {te}")
            raise te

        input_line = f"{ex_input_str_ansi}{ex_input_symbol_left}Input{ex_input_symbol_right}{self.ANSI_RESET}"
        input_line += f"{ex_input_data_ansi}{ex_input_data_symbol_left}{input_str}{ex_input_data_symbol_right}{self.ANSI_RESET}".replace(
            "\n",
            self.ANSI_RESET
            + "\n"
            + f"{ex_input_str_ansi}{ex_input_symbol_left}"
            + " " * (len(ex_input_symbol_right) + 5)
            + f"{self.ANSI_RESET}{ex_input_data_ansi}",
        )

        lines.append(input_line + "\n")

        # Output
        raw_output = example.get("output", "")
        out_str = self._html_to_ansi(raw_output)
        try:
            ex_output_str_ansi, ex_output_symbol_left, ex_output_symbol_right = (
                self.theme_manager.get_styling(
                    "PROBLEM_DESCRIPTION", "label_example_input"
                )
            )
            (
                ex_output_data_ansi,
                ex_output_data_symbol_left,
                ex_output_data_symbol_right,
            ) = self.theme_manager.get_styling(
                "PROBLEM_DESCRIPTION", "value_example_input"
            )

        except ThemeError as te:
            logger.error(f"Theming Error: {te}")
            raise te

        output_line = f"{ex_output_str_ansi}{ex_output_symbol_left}Output{ex_output_symbol_right}{self.ANSI_RESET}"
        output_line += f"{ex_output_data_ansi}{ex_output_data_symbol_left}{out_str}{ex_output_data_symbol_right}{self.ANSI_RESET}".replace(
            "\n",
            self.ANSI_RESET
            + "\n"
            + f"{ex_output_str_ansi}{ex_output_symbol_left}"
            + " " * (len(ex_output_symbol_right) + 6)
            + f"{self.ANSI_RESET}{ex_output_data_ansi}",
        )

        lines.append(output_line + "\n")

        # Explanation
        explanation = example.get("explanation", "")
        if explanation:
            expl_str = self._html_to_ansi(explanation)
            try:
                ex_expl_str_ansi, ex_expl_symbol_left, ex_expl_symbol_right = (
                    self.theme_manager.get_styling(
                        "PROBLEM_DESCRIPTION", "label_example_explanation"
                    )
                )
                (
                    ex_expl_data_ansi,
                    ex_expl_data_symbol_left,
                    ex_expl_data_symbol_right,
                ) = self.theme_manager.get_styling(
                    "PROBLEM_DESCRIPTION", "value_example_explanation"
                )

            except ThemeError as te:
                logger.error(f"Theming Error: {te}")
                raise te

            # Replace newline characters with formatted ANSI reset and new lines with symbols
            explanation_line = f"{ex_expl_str_ansi}{ex_expl_symbol_left}Explanation{ex_expl_symbol_right}{self.ANSI_RESET}"
            explanation_line += f"{ex_expl_data_ansi}{ex_expl_data_symbol_left}{expl_str}{ex_expl_data_symbol_right}{self.ANSI_RESET}".replace(
                "\n",
                self.ANSI_RESET
                + "\n"
                + f"{ex_expl_str_ansi}{ex_output_symbol_left}"
                + " " * (len(ex_expl_symbol_right) + 11)
                + f"{self.ANSI_RESET}{ex_expl_data_ansi}",
            )

            lines.append(explanation_line + "\n")

        return "".join(lines)
