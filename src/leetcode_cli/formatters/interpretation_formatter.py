from leetcode_cli.graphics.escape_sequences import ANSI_CODES, ANSI_RESET
from leetcode_cli.graphics.symbols import SYMBOLS
from leetcode_cli.models.interpretation import InterpretationResult
from leetcode_cli.utils.user_utils import load_formatting_config

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

class InterpretationFormatter:
    def __init__(self, result: InterpretationResult, testcases: str):
        self.result = result
        self.testcases = testcases
        self.format_conf = load_formatting_config()["interpretation"]

    def get_formatted_interpretation(self) -> str:
        status_code = self.result.status_code
        status_msg = self.result.status_msg
        lang = self.result.pretty_lang or self.result.lang
        total_testcases = self.result.total_testcases

        # Configuration flags
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

        # Error fields
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

            # Status line
            if status_code == 10:
                # Accepted or Wrong Answer depending on code_output vs expected_output
                if code_output == expected_output:
                    parsed_result += f"\n  {SUBMISSION_ANSI['Accepted']} Accepted {ANSI_RESET}\n"
                else:
                    parsed_result += f"\n  {SUBMISSION_ANSI['Wrong Answer']} Wrong Answer {ANSI_RESET}\n"
            else:
                ansi_status = SUBMISSION_ANSI.get(status_msg, SUBMISSION_ANSI["unknown"])
                parsed_result += f"\n  {ansi_status} {status_msg} {ANSI_RESET}\n"

            if show_language:
                parsed_result += _format_field('Language:', lang or "")

            if testcase and show_testcases:
                parsed_result += _format_field('Testcase:', ", ".join(testcase))

            if show_expected_output:
                parsed_result += _format_field('Expected Output:', expected_output)

            if show_code_output and code_output:
                parsed_result += _format_field('Your Output:', code_output)

            if show_stdout and std_output:
                parsed_result += _format_field('Stdout:', std_output)

            if show_errors:
                if runtime_error:
                    parsed_result += _format_field('Error Message:', runtime_error)

                if compile_error:
                    parsed_result += _format_field('Error Message:', compile_error)


            if detailed_errors:
                if full_runtime_error:
                    parsed_result += _format_field('Detailed Error:', full_runtime_error)

                if full_compile_error:
                    parsed_result += _format_field('Detailed Error:', full_compile_error)

        return parsed_result
