from leetcode_cli.utils.theme_utils import load_interpretation_theme_data
from leetcode_cli.graphics.ansi_codes import ANSI_RESET
from leetcode_cli.models.interpretation import InterpretationResult
from leetcode_cli.utils.formatting_config_utils import load_formatting_config
from leetcode_cli.exceptions.exceptions import ThemeError


class InterpretationFormatter:
    def __init__(self, result: InterpretationResult, testcases: str):
        self.result = result
        self.testcases = testcases
        self.format_conf = load_formatting_config()["interpretation"]

        try:
            self.THEME_DATA = load_interpretation_theme_data()

        except ThemeError as e:
            raise ThemeError(f"Failed to load interpretation theme: {str(e)}")

    def _format_field(self, label: str, value: str, width: int = 25) -> str:
        lines = value.split('\n')
        if not lines:
            return f"  {label:<{width}} \n"

        formatted = f"  {label:<{width}} {lines[0]}\n"
        padding = ' ' * (2 + width + 1)
        for line in lines[1:]:
            if line.strip() == "":
                continue
            formatted += f"{padding}{line}\n"
        return formatted

    def get_formatted_interpretation(self) -> str:
        status_code = self.result.status_code
        status_msg = self.result.status_msg
        lang = self.result.pretty_lang or self.result.lang
        total_testcases = self.result.total_testcases

        show_language = self.format_conf["show_language"]
        show_testcases = self.format_conf["show_testcases"]
        show_expected_output = self.format_conf["show_expected_output"]
        show_code_output = self.format_conf["show_code_output"]
        show_stdout = self.format_conf["show_stdout"]
        show_errors = self.format_conf["show_error_messages"]
        detailed_errors = self.format_conf["show_detailed_error_messages"]

        testcases_split = self.testcases.split("\n") if self.testcases else []
        parameters_in_testcase = len(testcases_split) // total_testcases if total_testcases else 1

        expected_outputs = self.result.expected_code_answer or []
        code_outputs = self.result.code_answer or []
        std_outputs = self.result.std_output_list or []

        runtime_error = getattr(self.result, 'runtime_error', None)
        full_runtime_error = getattr(self.result, 'full_runtime_error', None)
        compile_error = getattr(self.result, 'compile_error', None)
        full_compile_error = getattr(self.result, 'full_compile_error', None)

        parsed_result = ""

        for i, expected_output in enumerate(expected_outputs):
            if not expected_output:
                break

            testcase = testcases_split[i * parameters_in_testcase : i * parameters_in_testcase + parameters_in_testcase] if total_testcases else []
            code_output = code_outputs[i] if i < len(code_outputs) else None
            std_output = std_outputs[i] if i < len(std_outputs) else None

            if status_code == 10:
                # Accepted or Wrong Answer
                if code_output == expected_output:
                    parsed_result += f"\n  {self.THEME_DATA['INTERPRETATION_ANSI_CODES']['Accepted']}{self.THEME_DATA['INTERPRETATION_SYMBOLS']['Accepted']} Accepted {ANSI_RESET}\n"
                else:
                    parsed_result += f"\n  {self.THEME_DATA['INTERPRETATION_ANSI_CODES']['Wrong Answer']}{self.THEME_DATA['INTERPRETATION_SYMBOLS']['Wrong Answer']} Wrong Answer {ANSI_RESET}\n"
            else:
                ansi_status = self.THEME_DATA['INTERPRETATION_ANSI_CODES'].get(status_msg, self.THEME_DATA['INTERPRETATION_ANSI_CODES']["unknown"])
                parsed_result += f"\n  {ansi_status} {status_msg} {ANSI_RESET}\n"

            if show_language:
                parsed_result += self._format_field('Language:', lang or "")

            if testcase and show_testcases:
                parsed_result += self._format_field('Testcase:', ", ".join(testcase))

            if show_expected_output:
                parsed_result += self._format_field('Expected Output:', expected_output)

            if show_code_output and code_output:
                parsed_result += self._format_field('Your Output:', code_output)

            if show_stdout and std_output:
                parsed_result += self._format_field('Stdout:', std_output)

            if show_errors:
                if runtime_error:
                    parsed_result += self._format_field('Error Message:', runtime_error)
                if compile_error:
                    parsed_result += self._format_field('Error Message:', compile_error)

            if detailed_errors:
                if full_runtime_error:
                    parsed_result += self._format_field('Detailed Error:', full_runtime_error)
                if full_compile_error:
                    parsed_result += self._format_field('Detailed Error:', full_compile_error)

        return parsed_result
