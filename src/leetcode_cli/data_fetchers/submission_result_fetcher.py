import logging
import time

import requests

from leetcode_cli.exceptions.exceptions import FetchingError

logger = logging.getLogger(__name__)


def fetch_submission_result(
    cookie: str,
    csrf_token: str,
    title_slug: str,
    code: str,
    language: str,
    question_id: int,
) -> dict:
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

    logger.info("Submitting solution for '%s' in '%s'.", title_slug, language)

    try:
        response = requests.post(submit_url, json=payload, headers=headers)
        response.raise_for_status()
        submission = response.json()

    except requests.RequestException as e:
        logger.error("Submission failed for '%s': %s", title_slug, e)
        raise FetchingError(f"Submission failed: {e}") from e

    except ValueError:
        logger.error("Invalid JSON response for submission of '%s'.", title_slug)
        raise FetchingError("Invalid response format from LeetCode.") from None

    submission_id = submission.get("submission_id")
    if not submission_id:
        logger.error("No submission_id received for '%s'.", title_slug)
        raise FetchingError("Submission ID not received.")

    logger.debug("Got submission_id=%s, polling for result.", submission_id)

    check_submission_url = f"https://leetcode.com/submissions/detail/{submission_id}/check/"
    while True:
        try:
            r = requests.get(check_submission_url, headers=headers)
            r.raise_for_status()
            result = r.json()

        except requests.RequestException as e:
            logger.error("Failed to poll submission result: %s", e)
            raise FetchingError(f"Failed to check submission: {e}") from e

        except ValueError:
            logger.error("Invalid JSON while polling submission result.")
            raise FetchingError("Invalid response format.") from None

        state = result.get("state")
        logger.debug("Submission poll state: %s", state)

        if state == "SUCCESS":
            logger.info("Submission completed for '%s'.", title_slug)
            return result

        time.sleep(0.10)
