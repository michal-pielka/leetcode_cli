import time
import requests
import logging
import os

from ..user_utils import get_problem_by_key_value

logger = logging.getLogger(__name__)

class SubmissionError(Exception):
    """Custom exception for submission errors."""
    pass

def extract_submission_details(file_path):
    """
    Extracts question_id, title_slug, and file_extension from the given file_path.

    Args:
        file_path (str): Path to the solution file (e.g., /path/to/dir/1.two-sum.py).

    Returns:
        tuple: (question_id, title_slug, file_extension)

    Raises:
        SubmissionError: If the file_path format is incorrect.
    """
    filename = os.path.basename(file_path)
    parts = filename.split('.')
    if len(parts) < 3:
        raise SubmissionError("Solution file path is incorrect. Expected format: x.y.z (e.g., 1.two-sum.py).")
    
    frontend_question_id = parts[0]
    title_slug = '.'.join(parts[1:-1])  # Handles cases where title_slug contains dots
    file_extension = parts[-1].lower()
    
    if not frontend_question_id.isdigit():
        raise SubmissionError(f"Invalid question ID '{frontend_question_id}' in file path.")
    
    return frontend_question_id, title_slug, file_extension

def map_extension_to_language(file_extension):
    """
    Maps a file extension to its corresponding language slug.

    Args:
        file_extension (str): The file extension (e.g., 'py').

    Returns:
        str: The language slug (e.g., 'python').

    Raises:
        SubmissionError: If the file extension is unsupported.
    """
    extension_to_lang_slug = {
        "cpp": "cpp",
        "java": "java",
        "py": "python",
        "py3": "python3",
        "c": "c",
        "cs": "csharp",
        "js": "javascript",
        "ts": "typescript",
        "php": "php",
        "swift": "swift",
        "kt": "kotlin",
        "dart": "dart",
        "go": "golang",
        "rb": "ruby",
        "scala": "scala",
        "rs": "rust",
        "rkt": "racket",
        "erl": "erlang",
        "ex": "elixir"
    }
    
    lang_slug = extension_to_lang_slug.get(file_extension)
    if not lang_slug:
        raise SubmissionError(f"Unsupported file extension '{file_extension}'. Supported extensions are: {', '.join(extension_to_lang_slug.keys())}.")
    
    return lang_slug


def submit_solution(cookie: str, csrf_token: str, file_path: str) -> str:
    """
    Submits the solution code to LeetCode.

    Args:
        cookie (str): User authentication cookie.
        csrf_token (str): CSRF token extracted from the cookie.
        file_path (str): Path to the solution file (e.g., /path/to/dir/1.two-sum.py).

    Returns:
        str: The submission ID.

    Raises:
        SubmissionError: If submission fails.
    """
    try:
        frontend_question_id, title_slug, file_extension = extract_submission_details(file_path)
        question_id = get_problem_by_key_value("titleSlug", title_slug)["questionId"]

    except SubmissionError as e:
        raise SubmissionError(f"Error extracting submission details: {e}")

    submit_url = f"https://leetcode.com/problems/{title_slug}/submit/"

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()
    except IOError as e:
        raise SubmissionError(f"Error reading solution file: {e}")

    # Map file extension to language slug
    try:
        language = map_extension_to_language(file_extension)
    except SubmissionError as e:
        raise SubmissionError(e)

    # Create submission payload
    payload = {
        "lang": language,
        "question_id": str(question_id),
        "typed_code": code,
    }

    # Set headers
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Cookie": cookie,
        "x-csrftoken": csrf_token,
        "Referer": f"https://leetcode.com/problems/{title_slug}/",
    }

    # Submit code
    try:
        response = requests.post(submit_url, json=payload, headers=headers)
        response.raise_for_status()
        submission = response.json()
    except requests.RequestException as e:
        raise SubmissionError(f"Submission failed: {e}")
    except ValueError:
        raise SubmissionError("Invalid response format received from LeetCode.")

    submission_id = submission.get('submission_id')
    if not submission_id:
        raise SubmissionError("Submission ID not received.")

    return submission_id

def check_submission(cookie: str, csrf_token: str, submission_id: str, title_slug: str) -> dict:
    """
    Checks the status of the submission until it's complete.

    Args:
        cookie (str): User authentication cookie.
        csrf_token (str): CSRF token extracted from the cookie.
        submission_id (str): The submission ID.
        title_slug (str): The title slug of the problem.

    Returns:
        dict: The submission result data.

    Raises:
        SubmissionError: If checking submission fails.
    """
    check_submission_url = f"https://leetcode.com/submissions/detail/{submission_id}/check/"

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Cookie": cookie,
        "x-csrftoken": csrf_token,
        "Referer": f"https://leetcode.com/problems/{title_slug}/",
    }

    while True:
        try:
            response = requests.get(check_submission_url, headers=headers)
            response.raise_for_status()
            submission_result = response.json()
        except requests.RequestException as e:
            raise SubmissionError(f"Failed to check submission: {e}")
        except ValueError:
            raise SubmissionError("Invalid response format received from LeetCode.")

        if submission_result.get('state') == "SUCCESS":
            return submission_result

        time.sleep(0.25)  # Sleep for 250ms before the next check

def submit_and_get_result(cookie: str, csrf_token: str, file_path: str) -> dict:
    """
    Submits the solution and retrieves the result.

    Args:
        cookie (str): User authentication cookie.
        csrf_token (str): CSRF token extracted from the cookie.
        file_path (str): Path to the solution file.

    Returns:
        dict: The submission result data.

    Raises:
        SubmissionError: If submission or result retrieval fails.
    """
    # Submit the solution
    submission_id = submit_solution(cookie, csrf_token, file_path)

    # Extract title_slug from file_path for checking submission
    try:
        _, title_slug, _ = extract_submission_details(file_path)
    except SubmissionError as e:
        raise SubmissionError(f"Error extracting title_slug for checking submission: {e}")

    # Check the submission status
    submission_result = check_submission(cookie, csrf_token, submission_id, title_slug)
    return submission_result
