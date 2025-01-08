import requests
import time
from typing import Dict
from leetcode_cli.exceptions.exceptions import FetchingError


def fetch_submission_result(
    cookie: str,
    csrf_token: str,
    title_slug: str,
    code: str,
    language: str,
    question_id: int,
) -> Dict:
    """
    Fetches the final submission result from LeetCode (i.e., the "Submit" action).

    Args:
        cookie (str): User's session cookie.
        csrf_token (str): CSRF token for request validation.
        title_slug (str): The slug of the problem title.
        code (str): The user's code submission.
        language (str): The programming language of the submission.
        question_id (int): The unique identifier for the problem.

    Returns:
        Dict: The submission result.

    Raises:
        FetchingError: If any step in the process fails.
    """
    submit_url = f"https://leetcode.com/problems/{title_slug}/submit/"
    payload = {
        "lang": language,
        "question_id": str(question_id),
        "typed_code": code,
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Cookie": cookie,
        "x-csrftoken": csrf_token,
        "Referer": f"https://leetcode.com/problems/{title_slug}/",
    }

    try:
        response = requests.post(submit_url, json=payload, headers=headers)
        response.raise_for_status()
        submission = response.json()

    except requests.RequestException as e:
        raise FetchingError(f"Submission failed: {e}")

    except ValueError:
        raise FetchingError("Invalid response format from LeetCode.")

    submission_id = submission.get("submission_id")
    if not submission_id:
        raise FetchingError("Submission ID not received.")

    # Poll for final status
    check_submission_url = (
        f"https://leetcode.com/submissions/detail/{submission_id}/check/"
    )
    while True:
        try:
            r = requests.get(check_submission_url, headers=headers)
            r.raise_for_status()
            result = r.json()

        except requests.RequestException as e:
            raise FetchingError(f"Failed to check submission: {e}")

        except ValueError:
            raise FetchingError("Invalid response format.")

        if result.get("state") == "SUCCESS":
            return result

        time.sleep(0.10)
