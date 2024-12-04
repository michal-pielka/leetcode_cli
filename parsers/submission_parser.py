import logging
from ..graphics.escape_sequences import ANSI_CODES, ANSI_RESET
from ..graphics.symbols import SYMBOLS

# Define ANSI formatting for different submission statuses
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

# Configure logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)  # Set to DEBUG for detailed logs

class SubmissionParseError(Exception):
    """Custom exception for submission parsing errors."""
    pass


def get_formatted_interpretation(submission, testcases):
    status_code = submission.get("status_code", "unknow")   

    status_msg = submission.get("status_msg", "unknown")
    lang = submission.get("pretty_lang", None)

    total_testcases = submission.get("total_testcases", None)

    testcases_split = testcases.split("\n")
    parameters_in_testcase = len(testcases_split) // total_testcases

    expected_outputs = submission.get("expected_code_answer", [])
    code_outputs = submission.get("code_answer", []) # ["\"returning\"","\"returning\"","\"returning\"",""] 
    std_outputs = submission.get("std_output_list", [])

    error_msg1 = submission.get("runtime_error", None)
    error_msg2 = submission.get("compile_error", None)
    full_error_msg1 = submission.get("full_runtime_error")
    full_error_msg2 = submission.get("full_compile_error", None)

    parsed_result = ""

    for i in range(len(expected_outputs)):
        expected_output = expected_outputs[i]
        if not expected_output:
            break

        testcase = testcases_split[i * parameters_in_testcase : i * parameters_in_testcase + parameters_in_testcase]

        if i < len(code_outputs):
            code_output = code_outputs[i]
        else:
            code_output = None

        if i < len(std_outputs):
            std_output = std_outputs[i]
        else:
            std_output = None


        if status_code == 10:
            if code_output == expected_output:
                parsed_result += f"\n  {SUBMISSION_ANSI["Accepted"]} Accepted {ANSI_RESET}\n"
            else:
                parsed_result += f"\n  {SUBMISSION_ANSI["Wrong Answer"]} Wrong Answer {ANSI_RESET}\n"
        else:
            parsed_result += f"\n  {SUBMISSION_ANSI[status_msg]} {status_msg} {ANSI_RESET}\n"

        parsed_result += f"{_format_field('Language:', lang)}"


        if testcase:
            parsed_result += f"{_format_field('Testcase:', ", ".join(testcase))}"

        if expected_output:
            parsed_result += f"{_format_field('Expected Output:', expected_output)}"

        if code_output:
            parsed_result += f"{_format_field('Your Output:', code_output)}"

        if std_output:
            parsed_result += f"{_format_field('Stdout:', std_output)}"

        if error_msg1 != None:
            parsed_result += f"{_format_field("Error Message:", error_msg1)}"

        if full_error_msg1 != None:
            parsed_result += f"{_format_field("Detailed Error:", full_error_msg1)}"

        if error_msg2 != None:
            parsed_result += f"{_format_field("Error Message:", error_msg2)}"

        if full_error_msg2 != None:
            parsed_result += f"{_format_field("Detailed Error:", full_error_msg2)}"



    return parsed_result

def get_formatted_submission(submission):
    status_msg = submission.get("status_msg", "unknown")

    time_ms = submission.get("status_runtime", None)
    time_beats = submission.get("runtime_percentile", None)
    memory_size = submission.get("status_memory", None)
    memory_beats = submission.get("memory_percentile", None)
    total_correct = submission.get("total_correct", None)
    total_testcases = submission.get("total_testcases", None)
    lang = submission.get("pretty_lang", None)


    last_testcase = submission.get("last_testcase", None)
    expected_output = submission.get("expected_output", None)
    code_output = submission.get("code_output", None)
    std_output = submission.get("std_output", None)

    error_msg1 = submission.get("runtime_error", None)
    error_msg2 = submission.get("compile_error", None)
    full_error_msg1 = submission.get("full_runtime_error")
    full_error_msg2 = submission.get("full_compile_error", None)

    parsed_result = f"\n  {SUBMISSION_ANSI[status_msg]} {status_msg} {ANSI_RESET}\n"

    if total_correct != None and total_testcases != None:
        parsed_result += f"{_format_field('Passed testcases:', f'{total_correct} / {total_testcases}')}"

    parsed_result += f"{_format_field('Language:', lang)}"

    if time_ms != None and time_beats != None:
        formatted_time_beats = f"{time_beats:.2f}%"
        parsed_result += f"{_format_field('Runtime:', f'{time_ms} (Beats: {formatted_time_beats})')}"

    if memory_size != None and memory_beats != None:
        formatted_memory_beats = f"{memory_beats:.2f}%"
        parsed_result += f"{_format_field('Memory Usage:', f'{memory_size} (Beats: {formatted_memory_beats})')}"

    if last_testcase:
        parsed_result += f"{_format_field('Failed Testcase:', last_testcase.replace("\n", ", "))}"

    if expected_output:
        parsed_result += f"{_format_field('Expected Output:', expected_output)}"

    if code_output:
        parsed_result += f"{_format_field('Your Output:', code_output)}"

    if std_output:
        parsed_result += f"{_format_field("Stdout", std_output)}"

    if error_msg1 != None:
        parsed_result += f"{_format_field("Error Message:", error_msg1)}"

    if full_error_msg1 != None:
        parsed_result += f"{_format_field("Detailed Error:", full_error_msg1)}"

    if error_msg2 != None:
        parsed_result += f"{_format_field("Error Message:", error_msg2)}"

    if full_error_msg2 != None:
        parsed_result += f"{_format_field("Detailed Error:", full_error_msg2)}"

    return parsed_result

def _format_field(label: str, value: str, width: int = 25) -> str:
    """
    Formats a label-value pair with alignment.
    Handles multiline values by properly indenting subsequent lines.

    Args:
        label (str): The label for the field.
        value (str): The value of the field.
        width (int): The fixed width for the label.

    Returns:
        str: Formatted string with aligned label and value.
    """
    lines = value.split('\n')
    if not lines:
        return f"  {label:<{width}} \n"

    # Format the first line with the label
    formatted = f"  {label:<{width}} {lines[0]}\n"
    # Prepare indentation for subsequent lines
    padding = ' ' * (2 + width + 1)  # '  ' + label width + space
    for line in lines[1:]:
        if line.strip() == "":
            continue  # Skip empty lines to avoid excessive spacing
        formatted += f"{padding}{line}\n"
    return formatted
