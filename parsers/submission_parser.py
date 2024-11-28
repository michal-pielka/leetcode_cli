# TODO: Make the parsed message 'friendlier'
from ..graphics.colors import COLORS

def parse_submission(submission):
    status_code = submission.get("status_code")

    # Map status codes to their corresponding parser functions
    parsers = {
        10: parse_accepted,
        11: parse_wrong_answer,
        12: parse_memory_limit_exceeded,
        13: parse_output_limit_exceeded,
        14: parse_time_limit_exceeded,
        15: parse_runtime_error,
        20: parse_compile_error,
    }

    parse_function = parsers.get(status_code)
    if parse_function:
        return parse_function(submission)
    else:
        print("Unknown submission status code.")
        return None

def parse_accepted(submission):
    time_ms = submission.get("status_runtime", "N/A")
    memory_size = submission.get("status_memory", "N/A")

    parsed_result = (
        f"{COLORS["GREEN"]}Accepted{COLORS["RESET_COLOR"]}\n"
        f"Runtime: {time_ms}\n"
        f"Memory Usage: {memory_size}"
    )

    return parsed_result

def parse_wrong_answer(submission):
    last_testcase = submission.get("last_testcase", "")
    expected_output = submission.get("expected_output", "")
    code_output = submission.get("code_output", "")
    parsed_result = (
        f"{COLORS["RED"]}Wrong Answer{COLORS["RESET_COLOR"]}"
        f"Testcase: {last_testcase}\n"
        f"Expected Output: {expected_output}\n"
        f"Your Output: {code_output}"
    )

    return parsed_result

def parse_memory_limit_exceeded(submission):
    return f"{COLORS["RED"]}Memory Limit Exceeded{COLORS["RESET_COLOR"]}"

def parse_output_limit_exceeded(submission):
    return f"{COLORS["RED"]}Output Limit Exceeded{COLORS["RESET_COLOR"]}"

def parse_time_limit_exceeded(submission):
    return f"{COLORS["RED"]}Time Limit Exceeded{COLORS["RESET_COLOR"]}"

def parse_runtime_error(submission):
    error_msg = submission.get("runtime_error", "No error message.")
    return f"{COLORS["RED"]}Runtime Error{COLORS["RESET_COLOR"]}\n{error_msg}"

def parse_compile_error(submission):
    error_msg = submission.get("compile_error", "No error message.")
    return f"{COLORS["RED"]}Compile Error{COLORS["RESET_COLOR"]}\n{error_msg}"
