from leetcode_cli.graphics.escape_sequences import ANSI_CODES, ANSI_RESET
from leetcode_cli.graphics.symbols import SYMBOLS
from leetcode_cli.models.interpretation import InterpretationResult


# fetch result {'status_code': 15, 'lang': 'python', 'run_success': False, 'runtime_error': 'Line 3: TypeError: can only concatenate list (not "int") to list', 'full_runtime_error': 'TypeError: can only concatenate list (not "int") to list\n    dp = [0] * len(cost + 1)\nLine 3 in minCostClimbingStairs (Solution.py)\n    ret = Solution().minCostClimbingStairs(param_1)\nLine 34 in _driver (Solution.py)\n    _driver()\nLine 48 in <module> (Solution.py)', 'status_runtime': 'N/A', 'memory': 12172000, 'code_answer': [], 'code_output': [], 'std_output_list': [''], 'elapsed_time': 29, 'task_finish_time': 1733745588191, 'task_name': 'judger.runcodetask.RunCode', 'expected_status_code': 10, 'expected_lang': 'python', 'expected_run_success': True, 'expected_status_runtime': '15', 'expected_memory': 11972000, 'expected_display_runtime': '0', 'expected_code_answer': ['15', '6', ''], 'expected_code_output': [], 'expected_std_output_list': ['', '', ''], 'expected_elapsed_time': 32, 'expected_task_finish_time': 1733743435763, 'expected_task_name': 'judger.interprettask.Interpret', 'correct_answer': False, 'compare_result': '00', 'total_correct': 0, 'total_testcases': 2, 'runtime_percentile': None, 'status_memory': 'N/A', 'memory_percentile': None, 'pretty_lang': 'Python', 'submission_id': 'runcode_1733745585.9841516_FX0x9HkzTM', 'status_msg': 'Runtime Error', 'state': 'SUCCESS'}


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
        print("formatter:\n\n")
        print(self.result)
        status_code = self.result.status_code
        status_msg = self.result.status_msg
        lang = self.result.pretty_lang or self.result.lang
        total_testcases = self.result.total_testcases

        testcases_split = self.testcases.split("\n") if self.testcases else []
        parameters_in_testcase = len(testcases_split) // total_testcases if total_testcases else 1

        expected_outputs = self.result.expected_code_answer or []
        code_outputs = self.result.code_answer or []
        std_outputs = self.result.std_output_list or []

        error_msg1 = self.result.runtime_percentile
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
