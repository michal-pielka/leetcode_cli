import logging

from leetcode_cli.models.interpretation import InterpretationResult
from leetcode_cli.managers.theme_manager import ThemeManager
from leetcode_cli.exceptions.exceptions import ThemeError

logger = logging.getLogger(__name__)


class InterpretationFormatter:
    """
    Formats the 'run code' interpretation results, printing
    a separate "window" of info for each testcase, using the
    'INTERPRETATION' theme mappings. The styling and layout
    approach is similar to the SubmissionFormatter style.
    """

    def __init__(
        self,
        result: InterpretationResult,
        testcases_str: str,
        format_conf: dict,
        theme_manager: ThemeManager,
    ):
        self.result = result
        self.testcases_str = testcases_str
        self.format_conf = format_conf
        self.theme_manager = theme_manager
        self.theme_data = theme_manager.load_theme_data()

        self.ANSI_RESET = "\033[0m"  # Reset all styles

    def get_formatted_interpretation(self) -> str:
        status_code = self.result.status_code
        status_msg = self.result.status_msg
        lang = self.result.pretty_lang or self.result.lang
        total_testcases = self.result.total_testcases or 0

        show_language = self.format_conf.get("show_language", True)
        show_testcases = self.format_conf.get("show_testcases", True)
        show_expected_output = self.format_conf.get("show_expected_output", True)
        show_code_output = self.format_conf.get("show_code_output", True)
        show_stdout = self.format_conf.get("show_stdout", True)
        show_errors = self.format_conf.get("show_error_messages", True)
        detailed_errors = self.format_conf.get("show_detailed_error_messages", True)

        # Split testcases; each group of lines is one testcase's inputs
        testcases_split = self.testcases_str.split("\n") if self.testcases_str else []
        parameters_in_testcase = (
            len(testcases_split) // total_testcases if total_testcases > 0 else 1
        )

        expected_outputs = self.result.expected_code_answer or []
        code_outputs = self.result.code_answer or []
        std_outputs = self.result.std_output_list or []

        # Error fields
        runtime_error = self.result.runtime_error
        full_runtime_error = self.result.full_runtime_error
        compile_error = self.result.compile_error
        full_compile_error = self.result.full_compile_error

        parsed_result = ""

        # For each expected output => 1 testcase
        for i, expected_out in enumerate(expected_outputs):
            if not expected_out:
                break

            # Slice out the matching lines from testcases
            start_idx = i * parameters_in_testcase
            end_idx = start_idx + parameters_in_testcase
            testcase_lines = testcases_split[start_idx:end_idx]

            code_out = code_outputs[i] if i < len(code_outputs) else None
            stdout_line = std_outputs[i] if i < len(std_outputs) else None

            # Convert status_code -> status key
            if status_code == 10:
                # Typically 10 means 'Accepted' or 'Wrong Answer'
                status_key = "Accepted" if code_out == expected_out else "Wrong Answer"
            else:
                status_key = status_msg or "Unknown"

            # Retrieve style codes for the status
            try:
                s_ansi, s_left, s_right = self.theme_manager.get_styling(
                    "INTERPRETATION", "status_" + status_key.lower().replace(" ", "_")
                )
            except ThemeError as te:
                raise te

            # Print the status line, e.g. "  ✘ Wrong Answer"
            parsed_result += (
                f"\n  {s_ansi}{s_left}{status_key}{s_right}{self.ANSI_RESET}\n"
            )

            # Show fields
            if show_language:
                parsed_result += self._format_label_value("Language", lang)

            if show_testcases and testcase_lines:
                parsed_result += self._format_label_value(
                    "Testcase", ", ".join(testcase_lines)
                )

            if show_expected_output:
                parsed_result += self._format_label_value(
                    "Expected Output", expected_out
                )

            if show_code_output and code_out:
                parsed_result += self._format_label_value("Your Output", code_out)

            if show_stdout and stdout_line:
                parsed_result += self._format_label_value("Stdout", stdout_line)

            if show_errors:
                if runtime_error:
                    parsed_result += self._format_label_value(
                        "Error Message", runtime_error
                    )
                if compile_error:
                    parsed_result += self._format_label_value(
                        "Error Message", compile_error
                    )

            if detailed_errors:
                if full_runtime_error:
                    parsed_result += self._format_label_value(
                        "Detailed Error", full_runtime_error
                    )
                if full_compile_error:
                    parsed_result += self._format_label_value(
                        "Detailed Error", full_compile_error
                    )

        return parsed_result

    def _format_label_value(self, label: str, value: str) -> str:
        """
        High-level helper that calls _format_field_label and _format_field_value,
        returning a single line (plus potential newlines if value is multiline).
        """
        # Build the label portion (left-justified within some width)
        label_str = self._format_field_label(label)
        # The value portion
        value_str = self._format_field_value(value)

        # We'll place them on the same line separated by a space
        # If the value has multiple lines, we can handle that below
        lines = value_str.split("\n")
        if len(lines) == 1:
            # Single-line scenario
            return f"  {label_str} {lines[0]}\n"
        else:
            # Multi-line scenario: the first line goes with label, subsequent lines are padded
            first_line = f"  {label_str} {lines[0]}\n"
            # Each subsequent line is padded so that it lines up after the label
            padding = " " * (2 + 25 + 1)  # "  " + label_width(25) + 1 space
            subsequent = ""
            for l in lines[1:]:
                if l.strip():
                    subsequent += f"{padding}{l}\n"
            return first_line + subsequent

    def _format_field_label(self, label: str, width: int = 25) -> str:
        """
        Formats the field label using 'field_label' from INTERPRETATION.
        We left-justify label in a fixed-width area so columns align nicely.
        """
        try:
            ansi_code, sym_left, sym_right = self.theme_manager.get_styling(
                "INTERPRETATION", "label_field"
            )
        except ThemeError as te:
            logger.error(f"Theming Error: {te}")
            raise te

        # We combine label and the symbol_right (like a colon, if set in your theme).
        combined_label = f"{label}{sym_right}"
        # We left-justify within 'width' columns
        field_label = f"{ansi_code}{sym_left}{combined_label:<{width}}{self.ANSI_RESET}"
        return field_label

    def _format_field_value(self, value: str) -> str:
        """
        Formats the field value using 'field_value' from INTERPRETATION.
        """
        try:
            ansi_code, sym_left, sym_right = self.theme_manager.get_styling(
                "INTERPRETATION", "value_field"
            )
        except ThemeError as te:
            logger.error(f"Theming Error: {te}")
            raise te

        lines = value.split("\n")
        # Format each line separately so multi-line values work properly
        out_lines = []
        for idx, line in enumerate(lines):
            if not line.strip():
                # If the line is blank, we can skip or just preserve blank line
                out_lines.append("")
                continue
            out_lines.append(f"{ansi_code}{sym_left}{line}{sym_right}{self.ANSI_RESET}")
        return "\n".join(out_lines)
