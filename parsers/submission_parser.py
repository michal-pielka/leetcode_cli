from ..graphics.escape_sequences import ANSI_CODES, ANSI_RESET
import logging

logger = logging.getLogger(__name__)

def get_formatted_submission(submission: dict) -> str:
    status_code = submission.get("status_code")

    # Map status codes to their corresponding parser functions
    parsers = {
        10: _format_accepted,
        11: _format_wrong_answer,
        12: _format_memory_limit_exceeded,
        13: _format_output_limit_exceeded,
        14: _format_time_limit_exceeded,
        15: _format_runtime_error,
        20: _format_compile_error,
    }

    parse_function = parsers.get(status_code)
    if parse_function:
        return parse_function(submission)
    else:
        logger.error("Unknown submission status code.")
        return "Unknown submission status code."


def _format_accepted(submission: dict) -> str:
    time_ms = submission.get("status_runtime", "N/A")
    memory_size = submission.get("status_memory", "N/A")

    parsed_result = (
        f"{ANSI_CODES['GREEN']}Accepted{ANSI_RESET}\n"
        f"Runtime: {time_ms}\n"
        f"Memory Usage: {memory_size}"
    )

    return parsed_result


def _format_wrong_answer(submission: dict) -> str:
    last_testcase = submission.get("last_testcase", "")
    expected_output = submission.get("expected_output", "")
    code_output = submission.get("code_output", "")
    parsed_result = (
        f"{ANSI_CODES['RED']}Wrong Answer{ANSI_RESET}\n"
        f"Testcase: {last_testcase}\n"
        f"Expected Output: {expected_output}\n"
        f"Your Output: {code_output}"
    )

    return parsed_result


def _format_memory_limit_exceeded(submission: dict) -> str:
    return f"{ANSI_CODES['RED']}Memory Limit Exceeded{ANSI_RESET}"


def _format_output_limit_exceeded(submission: dict) -> str:
    return f"{ANSI_CODES['RED']}Output Limit Exceeded{ANSI_RESET}"


def _format_time_limit_exceeded(submission: dict) -> str:
    return f"{ANSI_CODES['RED']}Time Limit Exceeded{ANSI_RESET}"


def _format_runtime_error(submission: dict) -> str:
    error_msg = submission.get("runtime_error", "No error message.")
    return f"{ANSI_CODES['RED']}Runtime Error{ANSI_RESET}\n{error_msg}"


def _format_compile_error(submission: dict) -> str:
    error_msg = submission.get("compile_error", "No error message.")
    return f"{ANSI_CODES['RED']}Compile Error{ANSI_RESET}\n{error_msg}"
