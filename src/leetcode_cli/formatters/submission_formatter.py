from leetcode_cli.graphics.ansi_codes import ANSI_RESET
from leetcode_cli.models.submission import SubmissionResult
from leetcode_cli.services.theme_service import get_ansi_code, get_symbol
from leetcode_cli.models.theme import ThemeData

class SubmissionFormatter:
    def __init__(self, result: SubmissionResult, format_conf: dict, theme_data: ThemeData):
        self.result = result
        self.format_conf = format_conf
        self.theme_data = theme_data

    def get_formatted_submission(self) -> str:
        status_msg = self.result.status_msg

        show_language = self.format_conf.get("show_language", True)
        show_testcases = self.format_conf.get("show_testcases", True)
        show_runtime_memory = self.format_conf.get("show_runtime_memory", True)
        show_code_output = self.format_conf.get("show_code_output", True)
        show_stdout = self.format_conf.get("show_stdout", True)
        show_errors = self.format_conf.get("show_error_messages", True)
        detailed_errors = self.format_conf.get("show_detailed_error_messages", True)
        show_expected_output = self.format_conf.get("show_expected_output", True)

        time_ms = self.result.status_runtime
        time_beats = self.result.runtime_percentile
        memory_size = self.result.status_memory
        memory_beats = self.result.memory_percentile
        total_correct = self.result.total_correct
        total_testcases = self.result.total_testcases
        lang = self.result.pretty_lang or self.result.lang

        last_testcase = self.result.last_testcase
        expected_output = self.result.expected_output
        code_output = self.result.code_output
        std_output = self.result.std_output

        runtime_error = getattr(self.result, 'runtime_error', None)
        full_runtime_error = getattr(self.result, 'full_runtime_error', None)
        compile_error = getattr(self.result, 'compile_error', None)
        full_compile_error = getattr(self.result, 'full_compile_error', None)

        ansi_code = get_ansi_code(self.theme_data, 'SUBMISSION_ANSI_CODES', status_msg)
        symbol = get_symbol(self.theme_data, 'SUBMISSION_SYMBOLS', status_msg)

        ansi_status = f"{ansi_code}{symbol}{ANSI_RESET}"
        parsed_result = f"\n  {ansi_status} {status_msg} \n"

        if show_language and lang:
            parsed_result += self._format_field('Language:', lang or "")

        if show_testcases and total_correct is not None and total_testcases is not None:
            parsed_result += self._format_field('Passed Testcases:', f'{total_correct} / {total_testcases}')

        if show_runtime_memory:
            if time_ms and time_beats is not None:
                formatted_time_beats = f"{time_beats:.2f}%"
                parsed_result += self._format_field('Runtime:', f'{time_ms} (Beats: {formatted_time_beats})')

            if memory_size and memory_beats is not None:
                formatted_memory_beats = f"{memory_beats:.2f}%"
                parsed_result += self._format_field('Memory Usage:', f'{memory_size} (Beats: {formatted_memory_beats})')

        if last_testcase and show_testcases:
            parsed_result += self._format_field('Failed Testcase:', last_testcase.replace("\n", ", "))

        if show_expected_output and expected_output:
            parsed_result += self._format_field('Expected Output:', expected_output)

        if show_code_output and code_output:
            code_output_str = code_output if isinstance(code_output, str) else "\n".join(code_output)
            parsed_result += self._format_field('Your Output:', code_output_str)

        if show_stdout and std_output:
            std_output_str = std_output if isinstance(std_output, str) else "\n".join(std_output)
            parsed_result += self._format_field('Stdout:', std_output_str)

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
