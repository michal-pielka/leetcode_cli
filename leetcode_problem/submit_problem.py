import time
import requests
from user_utils import extract_csrf_token, get_cookie
from data_fetching.graphql_data_fetchers.leetcode_problem_fetcher import LeetCodeProblemFetcher
import logging

logger = logging.getLogger(__name__)


def map_extension_to_language(file_extension: str) -> str:
    extension_mapping = {
        "py": "python3",
        "js": "javascript",
        "ts": "typescript",
        "java": "java",
        "c": "c",
        "cpp": "cpp",
        "cs": "csharp",
        "rb": "ruby",
        "php": "php",
        "swift": "swift",
        "kt": "kotlin",
        "go": "golang",
        "rs": "rust",
        "scala": "scala",
        "sql": "mysql",
        "sh": "bash",
        "dart": "dart",
    }

    normalized_extension = file_extension.lstrip(".").lower()
    return extension_mapping.get(normalized_extension)


def submit_solution(cookie: str, title_slug: str, question_id: str, solution_file_path: str) -> str:
    submit_url = f"https://leetcode.com/problems/{title_slug}/submit/"
    csrf_token = extract_csrf_token(cookie)

    if not csrf_token:
        logger.error("CSRF token is None")
        return ""

    try:
        with open(solution_file_path, 'r', encoding='utf-8') as file:
            code = file.read()

    except IOError as e:
        logger.error(f"Error reading solution file: {e}")
        return ""

    # Determine language from file extension
    try:
        file_extension = solution_file_path[solution_file_path.rindex(".") + 1:]
    except ValueError:
        logger.error("Solution file path is incorrect.")
        return ""

    language = map_extension_to_language(file_extension)
    if not language:
        logger.error("Unknown file extension.")
        return ""

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
    response = requests.post(submit_url, json=payload, headers=headers)
    response.raise_for_status()
    submission = response.json()

    return submission.get('submission_id', "")


def check_submission(cookie: str, submission_id: str, title_slug: str) -> dict:
    check_submission_url = f"https://leetcode.com/submissions/detail/{submission_id}/check/"

    csrf_token = extract_csrf_token(cookie)

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Cookie": cookie,
        "x-csrftoken": csrf_token,
        "Referer": f"https://leetcode.com/problems/{title_slug}/",
    }

    while True:
        response = requests.get(check_submission_url, headers=headers)
        response.raise_for_status()
        submission_result = response.json()

        if submission_result.get('state') == "SUCCESS":
            return submission_result

        time.sleep(0.25)


def submit_and_get_result(cookie: str, title_slug: str, question_id: str, solution_file_path: str) -> dict:
    submission_id = submit_solution(cookie, title_slug, question_id, solution_file_path)

    if not submission_id:
        return {}

    submission_result = check_submission(cookie, submission_id, title_slug)
    return submission_result
