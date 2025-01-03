import logging

from leetcode_cli.graphics.ansi_codes import ANSI_RESET
from leetcode_cli.models.interpretation import InterpretationResult
from leetcode_cli.models.theme import ThemeData
from leetcode_cli.services.theme_service import get_styling
from leetcode_cli.exceptions.exceptions import ThemeError

logger = logging.getLogger(__name__)

class InterpretationFormatter:
    """
    Formats 'run code' interpretation results using (ansi, symbol_left, symbol_right) theming.
    """
    def __init__(self, result: InterpretationResult, testcases: str, format_conf: dict, theme_data: ThemeData):
        self.result = result
        self.testcases = testcases
        self.format_conf = format_conf
        self.theme_data = theme_data

    def _format_field_label(self, label: str, width: int = 25) -> str:
        """
        Formats the field label using the 'field_label' mapping.
        """
        try:
            ansi_code, symbol_left, symbol_right = get_styling(self.theme_data, "INTERPRETATION", "field_label")
        except ThemeError as te:
            logger.error(f"Theming Error: {te}")
            raise te

        # Combine label and symbol_right, then pad to width
        combined_label = f"{label}{symbol_right}"
        formatted_label = f"{ansi_code}{symbol_left}{combined_label:<{width}}{ANSI_RESET}"
        return formatted_label

    def _format_field_value(self, value: str) -> str:
        """
        Formats the field value using the 'field_value' mapping.
        """
        try:
            ansi_code, symbol_left, symbol_right = get_styling(self.theme_data, "INTERPRETATION", "field_value")
        except ThemeError as te:
            logger.error(f"Theming Error: {te}")
            raise te

        formatted_value = f"{ansi_code}{symbol_left}{value}{symbol_right}{ANSI_RESET}"
        return formatted_value

    def get_formatted_interpretation(self) -> str:
        status_code = self.result.status_code
        status_msg = self.result.status_msg
        lang = self.result.pretty_lang or self.result.lang
        total_testcases = self.result.total_testcases

        show_language = self.format_conf.get("show_language", True)
        show_testcases = self.format_conf.get("show_testcases", True)
        show_expected_output = self.format_conf.get("show_expected_output", True)
        show_code_output = self.format_conf.get("show_code_output", True)
        show_stdout = self.format_conf.get("show_stdout", True)
        show_errors = self.format_conf.get("show_error_messages", True)
        detailed_errors = self.format_conf.get("show_detailed_error_messages", True)

        testcases_split = self.testcases.split("\n") if self.testcases else []
        params_in_testcase = len(testcases_split) // total_testcases if total_testcases else 1

        code_outputs = self.result.code_answer or []
        expected_outputs = self.result.expected_code_answer or []
        stdouts = self.result.std_output_list or []

        runtime_error = self.result.runtime_error
        compile_error = self.result.compile_error
        full_runtime_error = self.result.full_runtime_error
        full_compile_error = self.result.full_compile_error

        parsed_result = ""

        for i, expected in enumerate(expected_outputs):
            if not expected:
                break

            testcase_lines = testcases_split[i * params_in_testcase : i * params_in_testcase + params_in_testcase]
            code_out = code_outputs[i] if i < len(code_outputs) else None
            stdout_line = stdouts[i] if i < len(stdouts) else None

            # Determine status key
            if status_code == 10:
                if code_out == expected:
                    status_key = "Accepted"
                else:
                    status_key = "Wrong Answer"
            else:
                status_key = status_msg  # Assuming status_msg corresponds to a key in mappings

            try:
                ansi_code, symbol_left, symbol_right = get_styling(self.theme_data, "INTERPRETATION", status_key)
            except ThemeError as te:
                logger.error(f"Theming Error: {te}")
                raise te

            parsed_result += f"\n  {ansi_code}{symbol_left}{status_key}{symbol_right}{ANSI_RESET}\n"

            # Format and append fields
            if show_language and lang:
                label = "Language"
                formatted_label = self._format_field_label(label)
                formatted_value = self._format_field_value(lang)
                parsed_result += f"  {formatted_label} {formatted_value}\n"

            if show_testcases and testcase_lines:
                label = "Testcase"
                formatted_label = self._format_field_label(label)
                formatted_value = self._format_field_value(", ".join(testcase_lines))
                parsed_result += f"  {formatted_label} {formatted_value}\n"

            if show_expected_output and expected:
                label = "Expected Output"
                formatted_label = self._format_field_label(label)
                formatted_value = self._format_field_value(expected)
                parsed_result += f"  {formatted_label} {formatted_value}\n"

            if show_code_output and code_out:
                label = "Your Output"
                formatted_label = self._format_field_label(label)
                formatted_value = self._format_field_value(code_out)
                parsed_result += f"  {formatted_label} {formatted_value}\n"

            if show_stdout and stdout_line:
                label = "Stdout"
                formatted_label = self._format_field_label(label)
                formatted_value = self._format_field_value(stdout_line)
                parsed_result += f"  {formatted_label} {formatted_value}\n"

            if show_errors:
                if runtime_error:
                    label = "Error Message"
                    formatted_label = self._format_field_label(label)
                    formatted_value = self._format_field_value(runtime_error)
                    parsed_result += f"  {formatted_label} {formatted_value}\n"
                    
                if compile_error:
                    label = "Error Message"
                    formatted_label = self._format_field_label(label)
                    formatted_value = self._format_field_value(compile_error)
                    parsed_result += f"  {formatted_label} {formatted_value}\n"

            if detailed_errors:
                if full_runtime_error:
                    label = "Detailed Error"
                    formatted_label = self._format_field_label(label)
                    formatted_value = self._format_field_value(full_runtime_error)
                    parsed_result += f"  {formatted_label} {formatted_value}\n"

                if full_compile_error:
                    label = "Detailed Error"
                    formatted_label = self._format_field_label(label)
                    formatted_value = self._format_field_value(full_compile_error)
                    parsed_result += f"  {formatted_label} {formatted_value}\n"

        return parsed_result
