# file: formatters/interpretation_result_formatter.py

import logging
from typing import Optional

from leetcode_cli.graphics.ansi_codes import ANSI_RESET
from leetcode_cli.models.interpretation import InterpretationResult
from leetcode_cli.managers.theme_manager import ThemeManager
from leetcode_cli.exceptions.exceptions import ThemeError

logger = logging.getLogger(__name__)

class InterpretationFormatter:
    """
    Formats the 'run code' interpretation results, printing a separate "window" of info
    for each testcase, using the 'INTERPRETATION' theme mappings.
    """

    def __init__(
        self,
        result: InterpretationResult,
        testcases_str: str,        # A single string of testcases separated by newlines
        format_conf: dict,
        theme_manager: ThemeManager
    ):
        self.result = result
        self.testcases_str = testcases_str      # We'll split this by '\n'
        self.format_conf = format_conf
        self.theme_manager = theme_manager

        # Pre-load theme data so we can do theming
        self.theme_data = self.theme_manager.load_theme_data()

    def _format_field(self, label: str, value: str, width: int = 25) -> str:
        """
        Formats a single field with label and value, applying 'field_label' / 'field_value'
        styling from the 'INTERPRETATION' section of the theme mappings.
        """
        try:
            label_ansi, label_left, label_right = self.theme_manager.get_styling("INTERPRETATION", "field_label")
            val_ansi, val_left, val_right = self.theme_manager.get_styling("INTERPRETATION", "field_value")

        except ThemeError as e:
            # If theme not found or invalid, log & fallback to no theming
            logger.warning(f"Theming Error: {e}; falling back to no styling.")
            label_ansi = val_ansi = ""
            label_left = val_left = ""
            label_right = val_right = ""
        
        lines = value.split('\n')
        if not lines:
            # If value is empty, just print label
            label_styled = f"{label_ansi}{label_left}{label}{label_right}{ANSI_RESET}"
            return f"  {label_styled:<{width}} \n"

        # First line of the value
        label_styled = f"{label_ansi}{label_left}{label}{label_right}{ANSI_RESET}"
        first_line = f"{val_ansi}{val_left}{lines[0]}{val_right}{ANSI_RESET}"
        formatted = f"  {label_styled:<{width}} {first_line}\n"

        # Subsequent lines are padded
        padding = ' ' * (2 + width + 1)
        for line in lines[1:]:
            if line.strip() == "":
                continue

            formatted += f"{padding}{val_ansi}{val_left}{line}{val_right}{ANSI_RESET}\n"

        return formatted

    def get_formatted_interpretation(self) -> str:
        status_code = self.result.status_code
        status_msg = self.result.status_msg
        lang = self.result.pretty_lang or self.result.lang
        total_testcases = self.result.total_testcases or 0

        # Configuration flags
        show_language = self.format_conf.get("show_language", True)
        show_testcases = self.format_conf.get("show_testcases", True)
        show_expected_output = self.format_conf.get("show_expected_output", True)
        show_code_output = self.format_conf.get("show_code_output", True)
        show_stdout = self.format_conf.get("show_stdout", True)
        show_errors = self.format_conf.get("show_error_messages", True)
        detailed_errors = self.format_conf.get("show_detailed_error_messages", True)

        # Split testcases by newline; each group of lines is one testcase's inputs
        testcases_split = self.testcases_str.split("\n") if self.testcases_str else []
        # If total_testcases is 3 and we have 6 lines, each testcase is 2 lines, etc.
        parameters_in_testcase = len(testcases_split) // total_testcases if total_testcases > 0 else 1

        # Interpretation's output arrays
        expected_outputs = self.result.expected_code_answer or []
        code_outputs = self.result.code_answer or []
        std_outputs = self.result.std_output_list or []

        # Error fields
        runtime_error = self.result.runtime_error
        full_runtime_error = self.result.full_runtime_error
        compile_error = self.result.compile_error
        full_compile_error = self.result.full_compile_error

        # Prepare the final string
        parsed_result = ""

        # We'll iterate over each "expected output," assuming that matches the count of testcases
        for i, expected_out in enumerate(expected_outputs):
            if not expected_out:
                break

            # Slice the correct lines from testcases_split
            start_idx = i * parameters_in_testcase
            end_idx = start_idx + parameters_in_testcase
            testcase_lines = testcases_split[start_idx:end_idx]

            # Attempt to figure out the code output, stdout, etc.
            code_out = code_outputs[i] if i < len(code_outputs) else None
            stdout_line = std_outputs[i] if i < len(std_outputs) else None

            # Convert status_code -> status key, or fallback to status_msg
            if status_code == 10:
                # Typically 10 means 'Accepted' or 'Wrong Answer'
                if code_out == expected_out:
                    status_key = "Accepted"
                else:
                    status_key = "Wrong Answer"
            else:
                status_key = status_msg or "unknown"

            # Attempt theming for the status. If not found, fallback to 'unknown'
            try:
                self.theme_manager.get_styling("INTERPRETATION", status_key)

            except ThemeError:
                status_key = "unknown"

            # Now apply the theming
            try:
                s_ansi, s_left, s_right = self.theme_manager.get_styling("INTERPRETATION", status_key)

            except ThemeError:
                # fallback if unknown
                s_ansi = ""
                s_left = ""
                s_right = ""

            # Print the status line, e.g. "  ✘ Wrong Answer"
            parsed_result += f"\n  {s_ansi}{s_left}{status_key}{s_right}{ANSI_RESET}\n"

            # Show fields
            if show_language:
                parsed_result += self._format_field("Language", lang or "")

            if show_testcases and testcase_lines:
                # Join them with a comma or space
                parsed_result += self._format_field("Testcase", ", ".join(testcase_lines))

            if show_expected_output:
                parsed_result += self._format_field("Expected Output", expected_out)

            if show_code_output and code_out:
                parsed_result += self._format_field("Your Output", code_out)

            if show_stdout and stdout_line:
                parsed_result += self._format_field("Stdout", stdout_line)

            if show_errors:
                if runtime_error:
                    parsed_result += self._format_field("Error Message", runtime_error)
                if compile_error:
                    parsed_result += self._format_field("Error Message", compile_error)

            if detailed_errors:
                if full_runtime_error:
                    parsed_result += self._format_field("Detailed Error", full_runtime_error)
                if full_compile_error:
                    parsed_result += self._format_field("Detailed Error", full_compile_error)

        return parsed_result
