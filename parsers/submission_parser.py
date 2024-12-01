from ..graphics.escape_sequences import ANSI_CODES, ANSI_RESET
import logging

logger = logging.getLogger(__name__)

# TODO: Make submissions friendlier

def parse_submission(submission: dict) -> str:
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
        logger.error("Unknown submission status code.")
        return "Unknown submission status code."


def parse_accepted(submission: dict) -> str:
    time_ms = submission.get("status_runtime", "N/A")
    memory_size = submission.get("status_memory", "N/A")

    parsed_result = (
        f"{ANSI_CODES['GREEN']}Accepted{ANSI_RESET}\n"
        f"Runtime: {time_ms}\n"
        f"Memory Usage: {memory_size}"
    )

    return parsed_result


def parse_wrong_answer(submission: dict) -> str:
    last_testcase = submission.get("last_testcase", "")
    expected_output = submission.get("expected_output", "")
    code_output = submission.get("code_output", "")
    parsed_result = (
        f"{ANSI_CODES['RED']}Wrong Answer{ANSI_CODES['RESET_COLOR']}\n"
        f"Testcase: {last_testcase}\n"
        f"Expected Output: {expected_output}\n"
        f"Your Output: {code_output}"
    )

    return parsed_result


def parse_memory_limit_exceeded(submission: dict) -> str:
    return f"{ANSI_CODES['RED']}Memory Limit Exceeded{ANSI_CODES['RESET_COLOR']}"


def parse_output_limit_exceeded(submission: dict) -> str:
    return f"{ANSI_CODES['RED']}Output Limit Exceeded{ANSI_CODES['RESET_COLOR']}"


def parse_time_limit_exceeded(submission: dict) -> str:
    return f"{ANSI_CODES['RED']}Time Limit Exceeded{ANSI_CODES['RESET_COLOR']}"


def parse_runtime_error(submission: dict) -> str:
    error_msg = submission.get("runtime_error", "No error message.")
    return f"{ANSI_CODES['RED']}Runtime Error{ANSI_CODES['RESET_COLOR']}\n{error_msg}"


def parse_compile_error(submission: dict) -> str:
    error_msg = submission.get("compile_error", "No error message.")
    return f"{ANSI_CODES['RED']}Compile Error{ANSI_CODES['RESET_COLOR']}\n{error_msg}"
