import logging

from leetcode_cli.graphics.ansi_codes import ANSI_RESET
from leetcode_cli.models.interpretation import InterpretationResult
from leetcode_cli.models.theme import ThemeData
from leetcode_cli.services.theme_service import get_styling
from leetcode_cli.exceptions.exceptions import ThemeError

logger = logging.getLogger(__name__)

class InterpretationFormatter:
    """
    Formats 'run code' interpretation results using (ansi, symbol) theming.
    """
    def __init__(self, result: InterpretationResult, testcases: str, format_conf: dict, theme_data: ThemeData):
        self.result = result
        self.testcases = testcases
        self.format_conf = format_conf
        self.theme_data = theme_data

    def _format_field(self, label: str, value: str, width: int = 25) -> str:
        """
        Formats a field with both label and value wrapped in ansi_code and symbol.
        """
        try:
            ansi_code, symbol = get_styling(self.theme_data, "INTERPRETATION", "field")

        except ThemeError as te:
            raise te

        lines = value.split('\n')
        if not lines:
            return f"  {ansi_code}{symbol}{label:<{width}} {ANSI_RESET}\n"

        formatted = f"  {ansi_code}{symbol}{label:<{width}} {lines[0]}{ANSI_RESET}\n"
        padding = ' ' * (2 + width + len(symbol))

        for line in lines[1:]:
            if line.strip() == "":
                continue

            formatted += f"{padding}{ansi_code}{symbol}{line}{ANSI_RESET}\n"

        return formatted

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

            if status_code == 10:
                if code_out == expected:
                    try:
                        ansi_code, symbol = get_styling(self.theme_data, "INTERPRETATION", "Accepted")

                    except ThemeError as te:
                        logger.error(f"Theming Error: {te}")
                        raise te

                    parsed_result += f"\n  {ansi_code}{symbol} Accepted{ANSI_RESET}\n"

                else:
                    try:
                        ansi_code, symbol = get_styling(self.theme_data, "INTERPRETATION", "Wrong Answer")

                    except ThemeError as te:
                        logger.error(f"Theming Error: {te}")
                        raise te

                    parsed_result += f"\n  {ansi_code}{symbol} Wrong Answer{ANSI_RESET}\n"
            else:
                try:
                    ansi_code, symbol = get_styling(self.theme_data, "INTERPRETATION", status_msg)

                except ThemeError as te:
                    logger.error(f"Theming Error: {te}")
                    raise te

                parsed_result += f"\n  {ansi_code}{symbol}{status_msg}{ANSI_RESET}\n"

            if show_language and lang:
                parsed_result += self._format_field("Language:", lang)

            if show_testcases and testcase_lines:
                parsed_result += self._format_field("Testcase:", ", ".join(testcase_lines))

            if show_expected_output and expected:
                parsed_result += self._format_field("Expected Output:", expected)

            if show_code_output and code_out:
                parsed_result += self._format_field("Your Output:", code_out)

            if show_stdout and stdout_line:
                parsed_result += self._format_field("Stdout:", stdout_line)

            if show_errors:
                if runtime_error:
                    parsed_result += self._format_field("Error Message:", runtime_error)
                    
                if compile_error:
                    parsed_result += self._format_field("Error Message:", compile_error)

            if detailed_errors:
                if full_runtime_error:
                    parsed_result += self._format_field("Detailed Error:", full_runtime_error)

                if full_compile_error:
                    parsed_result += self._format_field("Detailed Error:", full_compile_error)

        return parsed_result
