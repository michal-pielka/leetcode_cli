from leetcode_cli.graphics.escape_sequences import ANSI_CODES, ANSI_RESET
from leetcode_cli.graphics.symbols import SYMBOLS
from leetcode_cli.parsers.submission_parser import SubmissionParseError
from leetcode_cli.models.interpretation import InterpretationResult

# Reuse SUBMISSION_ANSI from previous code
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

    def get_formatted_interpretation(self) -> str:
        status_code = self.result.status_code
        status_msg = self.result.status_msg
        lang = self.result.pretty_lang or self.result.lang
        total_testcases = self.result.total_testcases

        testcases_split = self.testcases.split("\n") if self.testcases else []
        parameters_in_testcase = len(testcases_split) // total_testcases if total_testcases else 1

        expected_outputs = self.result.expected_code_answer or []
        code_outputs = self.result.code_answer or []
        std_outputs = self.result.std_output_list or []

        error_msg1 = self.result.runtime_percentile  # Correction: runtime_percentile not error msg?
        # Actually from old code, error_msg1 should be from runtime_error, compile_error fields
        # Let's add runtime_error and compile_error fields to InterpretationResult if missing
        # Re-check sample: it has runtime_error and compile_error possibly.
        # Let's handle errors from the initial model fields if needed:
        # The initial code references error_msg1, error_msg2 from submission dictionary
        # Let's just assume we have runtime_error and compile_error in the InterpretationResult model.
        # Add them in model and handle here:
        error_msg1 = getattr(self.result, 'runtime_error', None)
        error_msg2 = getattr(self.result, 'compile_error', None)
        full_error_msg1 = getattr(self.result, 'full_runtime_error', None)
        full_error_msg2 = getattr(self.result, 'full_compile_error', None)

        parsed_result = ""

        for i, expected_output in enumerate(expected_outputs):
            if not expected_output:
                break

            testcase = testcases_split[i * parameters_in_testcase : i * parameters_in_testcase + parameters_in_testcase] if total_testcases else []

            code_output = code_outputs[i] if i < len(code_outputs) else None
            std_output = std_outputs[i] if i < len(std_outputs) else None

            # Check status_code 10 = Accepted logic from old code
            # If status_code == 10 and code_output == expected_output => Accepted else Wrong Answer
            # Otherwise, use status_msg mapping
            # For interpretation, "status_code":10 and "status_msg":"Accepted"
            if status_code == 10:
                if code_output == expected_output:
                    parsed_result += f"\n  {SUBMISSION_ANSI['Accepted']} Accepted {ANSI_RESET}\n"
                else:
                    parsed_result += f"\n  {SUBMISSION_ANSI['Wrong Answer']} Wrong Answer {ANSI_RESET}\n"
            else:
                ansi_status = SUBMISSION_ANSI.get(status_msg, SUBMISSION_ANSI["unknown"])
                parsed_result += f"\n  {ansi_status} {status_msg} {ANSI_RESET}\n"

            parsed_result += _format_field('Language:', lang or "")

            if testcase:
                parsed_result += _format_field('Testcase:', ", ".join(testcase))

            parsed_result += _format_field('Expected Output:', expected_output)

            if code_output:
                parsed_result += _format_field('Your Output:', code_output)

            if std_output:
                parsed_result += _format_field('Stdout:', std_output)

            if error_msg1 is not None:
                parsed_result += _format_field('Error Message:', error_msg1)

            if full_error_msg1 is not None:
                parsed_result += _format_field('Detailed Error:', full_error_msg1)

            if error_msg2 is not None:
                parsed_result += _format_field('Error Message:', error_msg2)

            if full_error_msg2 is not None:
                parsed_result += _format_field('Detailed Error:', full_error_msg2)

        return parsed_result
