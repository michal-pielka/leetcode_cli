from leetcode_cli.graphics.escape_sequences import ANSI_CODES, ANSI_RESET
from leetcode_cli.graphics.symbols import SYMBOLS
from leetcode_cli.models.submission import SubmissionResult

SUBMISSION_ANSI = {
    "Accepted": ANSI_CODES["GREEN"] + ANSI_CODES["BOLD"] + SYMBOLS["CHECKMARK"],
    "Wrong Answer": ANSI_CODES["RED"] + ANSI_CODES["BOLD"] + SYMBOLS["X"],
    "Memory Limit Exceeded": ANSI_CODES["RED"] + ANSI_CODES["BOLD"] + SYMBOLS["X"],
    "Output Limit Exceeded": ANSI_CODES["RED"] + ANSI_CODES["BOLD"] + SYMBOLS["X"],
    "Time Limit Exceeded": ANSI_CODES["RED"] + ANSI_CODES["BOLD"] + SYMBOLS["X"],
    "Runtime Error": ANSI_CODES["RED"] + ANSI_CODES["BOLD"] + SYMBOLS["X"],
    "Compile Error": ANSI_CODES["RED"] + ANSI_CODES["BOLD"] + SYMBOLS["X"],
    "unknown": ANSI_CODES["ORANGE"] + ANSI_CODES["BOLD"] + SYMBOLS["X"],
}

def _format_field(label: str, value: str, width: int = 25) -> str:
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

class SubmissionFormatter:
    def __init__(self, result: SubmissionResult):
        self.result = result

    def get_formatted_submission(self) -> str:
        status_msg = self.result.status_msg

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

        # If runtime_error or compile_error fields exist, handle them similarly to interpretation
        error_msg1 = getattr(self.result, 'runtime_error', None)
        error_msg2 = getattr(self.result, 'compile_error', None)
        full_error_msg1 = getattr(self.result, 'full_runtime_error', None)
        full_error_msg2 = getattr(self.result, 'full_compile_error', None)

        ansi_status = SUBMISSION_ANSI.get(status_msg, SUBMISSION_ANSI["unknown"])

        parsed_result = f"\n  {ansi_status} {status_msg} {ANSI_RESET}\n"

        if total_correct is not None and total_testcases is not None:
            parsed_result += _format_field('Passed testcases:', f'{total_correct} / {total_testcases}')

        parsed_result += _format_field('Language:', lang or "")

        if time_ms is not None and time_beats is not None:
            formatted_time_beats = f"{time_beats:.2f}%"
            parsed_result += _format_field('Runtime:', f'{time_ms} (Beats: {formatted_time_beats})')

        if memory_size is not None and memory_beats is not None:
            formatted_memory_beats = f"{memory_beats:.2f}%"
            parsed_result += _format_field('Memory Usage:', f'{memory_size} (Beats: {formatted_memory_beats})')

        if last_testcase:
            parsed_result += _format_field('Failed Testcase:', last_testcase.replace("\n", ", "))

        if expected_output:
            parsed_result += _format_field('Expected Output:', expected_output)

        if code_output:
            parsed_result += _format_field('Your Output:', code_output)

        if std_output:
            parsed_result += _format_field('Stdout', std_output)

        if error_msg1 is not None:
            parsed_result += _format_field('Error Message:', error_msg1)

        if full_error_msg1 is not None:
            parsed_result += _format_field('Detailed Error:', full_error_msg1)

        if error_msg2 is not None:
            parsed_result += _format_field('Error Message:', error_msg2)

        if full_error_msg2 is not None:
            parsed_result += _format_field('Detailed Error:', full_error_msg2)

        return parsed_result
