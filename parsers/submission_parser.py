from datetime import datetime
from re import sub
from ..graphics.escape_sequences import ANSI_CODES, ANSI_RESET
from ..graphics.symbols import SYMBOLS
import logging

import logging
from datetime import datetime

# Define ANSI escape codes for text formatting
ANSI_CODES = {
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "YELLOW": "\033[93m",
    "BLUE": "\033[94m",
    "MAGENTA": "\033[95m",
    "CYAN": "\033[96m",
    "BOLD": "\033[1m",
    "UNDERLINE": "\033[4m",
}

# Reset ANSI formatting
ANSI_RESET = "\033[0m"

# Define symbols used in the output
SYMBOLS = {
    "CHECKMARK": "✔",
    "CROSS": "✖",
    "WARNING": "⚠",
    "ERROR": "🛑",
    "CLOCK": "⏰",
    "INFO": "ℹ",
}

# Define ANSI formatting for different submission statuses
SUBMISSION_ANSI = {
    "accepted": ANSI_CODES["GREEN"] + ANSI_CODES["BOLD"] + SYMBOLS["CHECKMARK"],
    "wrong_answer": ANSI_CODES["RED"] + ANSI_CODES["BOLD"] + SYMBOLS["CROSS"],
    "memory_limit_exceeded": ANSI_CODES["RED"] + ANSI_CODES["BOLD"] + "MLE",
    "output_limit_exceeded": ANSI_CODES["RED"] + ANSI_CODES["BOLD"] + "OLE",
    "time_limit_exceeded": ANSI_CODES["RED"] + ANSI_CODES["BOLD"] + "TLE",
    "runtime_error": ANSI_CODES["RED"] + ANSI_CODES["BOLD"] + "RE",
    "compile_error": ANSI_CODES["RED"] + ANSI_CODES["BOLD"] + "CE",
    "unknown": ANSI_CODES["YELLOW"] + ANSI_CODES["BOLD"] + SYMBOLS["WARNING"],
}

# Configure logging
logger = logging.getLogger(__name__)

class SubmissionParseError(Exception):
    """Custom exception for submission parsing errors."""
    pass

def _format_field(label: str, value: str, width: int = 25) -> str:
    """
    Formats a label-value pair with alignment.

    Args:
        label (str): The label for the field.
        value (str): The value of the field.
        width (int): The fixed width for the label.

    Returns:
        str: Formatted string with aligned label and value.
    """
    return f"  {label:<{width}} {value}\n"

def _format_accepted(submission: dict) -> str:
    """
    Formats an accepted submission.

    Args:
        submission (dict): The submission data.

    Returns:
        str: Formatted string for an accepted submission.
    """
    try:
        time_ms = submission.get("status_runtime", "N/A")
        time_beats = submission.get("runtime_percentile", "N/A")
        memory_size = submission.get("status_memory", "N/A")
        memory_beats = submission.get("memory_percentile", "N/A")
        submission_id = submission.get("submission_id", "N/A")
        lang = submission.get("lang", "N/A")
        question_id = submission.get("question_id", "N/A")
        question_title = submission.get("question_title", "N/A")
        timestamp = submission.get("submission_timestamp", None)
        submission_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else "N/A"

        # Format beats percentages to two decimal places
        if isinstance(time_beats, (int, float)):
            time_beats = f"{time_beats:.2f}"
        if isinstance(memory_beats, (int, float)):
            memory_beats = f"{memory_beats:.2f}"

        parsed_result = (
            f"\n  {SUBMISSION_ANSI['accepted']} Accepted {ANSI_RESET}\n"
            f"{_format_field('Question ID:', f'[{question_id}] {question_title}')}"
            f"{_format_field('Language:', lang)}"
            f"{_format_field('Submission ID:', submission_id)}"
            f"{_format_field('Submitted at:', submission_time)}"
            f"{_format_field('Runtime:', f'{time_ms} ms (Beat: {time_beats}%)')}"
            f"{_format_field('Memory Usage:', f'{memory_size} KB (Beat: {memory_beats}%)')}"
        )
        return parsed_result
    except Exception as e:
        logger.error(f"Error formatting accepted submission: {e}")
        raise SubmissionParseError("Failed to format accepted submission.") from e

def _format_wrong_answer(submission: dict) -> str:
    """
    Formats a wrong answer submission.

    Args:
        submission (dict): The submission data.

    Returns:
        str: Formatted string for a wrong answer submission.
    """
    try:
        last_testcase = submission.get("last_testcase", "N/A")
        expected_output = submission.get("expected_output", "N/A")
        code_output = submission.get("code_output", "N/A")
        std_output = submission.get("std_output", "N/A")
        submission_id = submission.get("submission_id", "N/A")
        lang = submission.get("lang", "N/A")
        question_id = submission.get("question_id", "N/A")
        question_title = submission.get("question_title", "N/A")
        timestamp = submission.get("submission_timestamp", None)
        submission_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else "N/A"

        parsed_result = (
            f"\n{SUBMISSION_ANSI['wrong_answer']} Wrong Answer {ANSI_RESET}\n"
            f"{_format_field('Question ID:', f'[{question_id}] {question_title}')}"
            f"{_format_field('Language:', lang)}"
            f"{_format_field('Submission ID:', submission_id)}"
            f"{_format_field('Submitted at:', submission_time)}"
            f"{_format_field('Failed Testcase:', last_testcase)}"
            f"{_format_field('Expected Output:', expected_output)}"
            f"{_format_field('Your Output:', code_output)}"
            f"{_format_field('Std Output:', std_output)}"
        )
        return parsed_result
    except Exception as e:
        logger.error(f"Error formatting wrong answer submission: {e}")
        raise SubmissionParseError("Failed to format wrong answer submission.") from e

def _format_memory_limit_exceeded(submission: dict) -> str:
    """
    Formats a memory limit exceeded submission.

    Args:
        submission (dict): The submission data.

    Returns:
        str: Formatted string for a memory limit exceeded submission.
    """
    try:
        memory_limit = submission.get("memory_limit", "N/A")
        memory_used = submission.get("memory_used", "N/A")
        submission_id = submission.get("submission_id", "N/A")
        lang = submission.get("lang", "N/A")
        question_id = submission.get("question_id", "N/A")
        question_title = submission.get("question_title", "N/A")
        timestamp = submission.get("submission_timestamp", None)
        submission_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else "N/A"

        parsed_result = (
            f"\n{SUBMISSION_ANSI['memory_limit_exceeded']} Memory Limit Exceeded {ANSI_RESET}\n"
            f"{_format_field('Question ID:', f'[{question_id}] {question_title}')}"
            f"{_format_field('Language:', lang)}"
            f"{_format_field('Submission ID:', submission_id)}"
            f"{_format_field('Submitted at:', submission_time)}"
            f"{_format_field('Memory Limit:', f'{memory_limit} KB')}"
            f"{_format_field('Memory Used:', f'{memory_used} KB')}"
        )
        return parsed_result
    except Exception as e:
        logger.error(f"Error formatting memory limit exceeded submission: {e}")
        raise SubmissionParseError("Failed to format memory limit exceeded submission.") from e

def _format_output_limit_exceeded(submission: dict) -> str:
    """
    Formats an output limit exceeded submission.

    Args:
        submission (dict): The submission data.

    Returns:
        str: Formatted string for an output limit exceeded submission.
    """
    try:
        output_limit = submission.get("output_limit", "N/A")
        output_size = submission.get("output_size", "N/A")
        submission_id = submission.get("submission_id", "N/A")
        lang = submission.get("lang", "N/A")
        question_id = submission.get("question_id", "N/A")
        question_title = submission.get("question_title", "N/A")
        timestamp = submission.get("submission_timestamp", None)
        submission_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else "N/A"

        parsed_result = (
            f"\n{SUBMISSION_ANSI['output_limit_exceeded']} Output Limit Exceeded {ANSI_RESET}\n"
            f"{_format_field('Question ID:', f'[{question_id}] {question_title}')}"
            f"{_format_field('Language:', lang)}"
            f"{_format_field('Submission ID:', submission_id)}"
            f"{_format_field('Submitted at:', submission_time)}"
            f"{_format_field('Output Limit:', f'{output_limit} KB')}"
            f"{_format_field('Output Size:', f'{output_size} KB')}"
        )
        return parsed_result
    except Exception as e:
        logger.error(f"Error formatting output limit exceeded submission: {e}")
        raise SubmissionParseError("Failed to format output limit exceeded submission.") from e

def _format_time_limit_exceeded(submission: dict) -> str:
    """
    Formats a time limit exceeded submission.

    Args:
        submission (dict): The submission data.

    Returns:
        str: Formatted string for a time limit exceeded submission.
    """
    try:
        time_limit = submission.get("time_limit", "N/A")
        time_used = submission.get("time_used", "N/A")
        submission_id = submission.get("submission_id", "N/A")
        lang = submission.get("lang", "N/A")
        question_id = submission.get("question_id", "N/A")
        question_title = submission.get("question_title", "N/A")
        timestamp = submission.get("submission_timestamp", None)
        submission_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else "N/A"

        parsed_result = (
            f"\n{SUBMISSION_ANSI['time_limit_exceeded']} Time Limit Exceeded {ANSI_RESET}\n"
            f"{_format_field('Question ID:', f'[{question_id}] {question_title}')}"
            f"{_format_field('Language:', lang)}"
            f"{_format_field('Submission ID:', submission_id)}"
            f"{_format_field('Submitted at:', submission_time)}"
            f"{_format_field('Time Limit:', f'{time_limit} ms')}"
            f"{_format_field('Time Used:', f'{time_used} ms')}"
        )
        return parsed_result
    except Exception as e:
        logger.error(f"Error formatting time limit exceeded submission: {e}")
        raise SubmissionParseError("Failed to format time limit exceeded submission.") from e

def _format_runtime_error(submission: dict) -> str:
    """
    Formats a runtime error submission.

    Args:
        submission (dict): The submission data.

    Returns:
        str: Formatted string for a runtime error submission.
    """
    try:
        error_msg = submission.get("runtime_error", "No error message.")
        full_error_msg = submission.get("full_runtime_error", "No detailed error message.")
        submission_id = submission.get("submission_id", "N/A")
        lang = submission.get("lang", "N/A")
        question_id = submission.get("question_id", "N/A")
        question_title = submission.get("question_title", "N/A")
        timestamp = submission.get("submission_timestamp", None)
        submission_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else "N/A"

        parsed_result = (
            f"\n{SUBMISSION_ANSI['runtime_error']} Runtime Error {ANSI_RESET}\n"
            f"{_format_field('Question ID:', f'[{question_id}] {question_title}')}"
            f"{_format_field('Language:', lang)}"
            f"{_format_field('Submission ID:', submission_id)}"
            f"{_format_field('Submitted at:', submission_time)}"
            f"{_format_field('Error Message:', error_msg)}"
            f"{_format_field('Detailed Error:', full_error_msg)}"
        )
        return parsed_result
    except Exception as e:
        logger.error(f"Error formatting runtime error submission: {e}")
        raise SubmissionParseError("Failed to format runtime error submission.") from e

def _format_compile_error(submission: dict) -> str:
    """
    Formats a compile error submission.

    Args:
        submission (dict): The submission data.

    Returns:
        str: Formatted string for a compile error submission.
    """
    try:
        error_msg = submission.get("compile_error", "No compile error message.")
        submission_id = submission.get("submission_id", "N/A")
        lang = submission.get("lang", "N/A")
        question_id = submission.get("question_id", "N/A")
        question_title = submission.get("question_title", "N/A")
        timestamp = submission.get("submission_timestamp", None)
        submission_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else "N/A"

        parsed_result = (
            f"\n{SUBMISSION_ANSI['compile_error']} Compile Error {ANSI_RESET}\n"
            f"{_format_field('Question ID:', f'[{question_id}] {question_title}')}"
            f"{_format_field('Language:', lang)}"
            f"{_format_field('Submission ID:', submission_id)}"
            f"{_format_field('Submitted at:', submission_time)}"
            f"{_format_field('Error Message:', error_msg)}"
        )
        return parsed_result
    except Exception as e:
        logger.error(f"Error formatting compile error submission: {e}")
        raise SubmissionParseError("Failed to format compile error submission.") from e

def _format_unknown_status(submission: dict) -> str:
    """
    Formats an unknown submission status.

    Args:
        submission (dict): The submission data.

    Returns:
        str: Formatted string for an unknown submission status.
    """
    try:
        status_code = submission.get("status_code", "N/A")
        message = submission.get("message", "No additional information.")
        submission_id = submission.get("submission_id", "N/A")
        lang = submission.get("lang", "N/A")
        question_id = submission.get("question_id", "N/A")
        question_title = submission.get("question_title", "N/A")
        timestamp = submission.get("submission_timestamp", None)
        submission_time = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S') if timestamp else "N/A"

        parsed_result = (
            f"\n{SUBMISSION_ANSI['unknown']} Unknown Status ({status_code}) {ANSI_RESET}\n"
            f"{_format_field('Question ID:', f'[{question_id}] {question_title}')}"
            f"{_format_field('Language:', lang)}"
            f"{_format_field('Submission ID:', submission_id)}"
            f"{_format_field('Submitted at:', submission_time)}"
            f"{_format_field('Message:', message)}"
        )
        return parsed_result
    except Exception as e:
        logger.error(f"Error formatting unknown status submission: {e}")
        raise SubmissionParseError("Failed to format unknown status submission.") from e

def get_formatted_submission(submission: dict) -> str:
    """
    Parses the submission result and returns a formatted string.

    Args:
        submission (dict): The submission result data.

    Returns:
        str: A formatted string representing the submission result.

    Raises:
        SubmissionParseError: If the submission data is missing or invalid.
    """
    if not submission:
        logger.error("Submission data is empty.")
        raise SubmissionParseError("Submission data is empty.")

    status_code = submission.get("status_code")
    logger.debug(f"Processing submission with status code: {status_code}")

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

    parse_function = parsers.get(status_code, _format_unknown_status)
    logger.debug(f"Using parser function: {parse_function.__name__}")

    return parse_function(submission)
