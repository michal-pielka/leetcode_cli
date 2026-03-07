import logging
import time

import requests

from leetcode_cli.exceptions.exceptions import FetchingError

logger = logging.getLogger(__name__)


def fetch_interpretation_result(
    cookie: str,
    csrf_token: str,
    title_slug: str,
    code: str,
    language: str,
    testcases: str,
    question_id: int,
) -> dict:
    """
    Fetch the 'Run Code' / interpretation result from LeetCode for a given problem.

    Args:
        cookie (str): User's session cookie.
        csrf_token (str): CSRF token for request validation.
        title_slug (str): The slug of the problem title.
        code (str): The user's code submission.
        language (str): The programming language of the submission.
        testcases (str): Testcases input as a string.
        question_id (int): The unique identifier for the problem.

    Returns:
        Dict: The interpretation result.

    Raises:
        FetchingError: If any step in the process fails.
    """
    submit_url = f"https://leetcode.com/problems/{title_slug}/interpret_solution/"
    payload = {
        "data_input": testcases,
        "lang": language,
        "question_id": question_id,
        "typed_code": code,
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Cookie": cookie,
        "x-csrftoken": csrf_token,
        "Referer": f"https://leetcode.com/problems/{title_slug}/",
    }

    logger.info("Submitting interpretation for '%s' in '%s'.", title_slug, language)

    try:
        response = requests.post(submit_url, json=payload, headers=headers)
        response.raise_for_status()
        submission = response.json()

    except requests.RequestException as e:
        logger.error("Interpretation submission failed for '%s': %s", title_slug, e)
        raise FetchingError(f"Submission failed: {e}")

    except ValueError:
        logger.error("Invalid JSON response for interpretation of '%s'.", title_slug)
        raise FetchingError("Invalid response format from LeetCode.")

    interpret_id = submission.get("interpret_id")
    if not interpret_id:
        logger.error("No interpret_id received for '%s'.", title_slug)
        raise FetchingError("Interpretation ID not received.")

    logger.debug("Got interpret_id=%s, polling for result.", interpret_id)

    check_submission_url = f"https://leetcode.com/submissions/detail/{interpret_id}/check/"
    while True:
        try:
            r = requests.get(check_submission_url, headers=headers)
            r.raise_for_status()
            result = r.json()

        except requests.RequestException as e:
            logger.error("Failed to poll interpretation result: %s", e)
            raise FetchingError(f"Failed to check interpretation: {e}")

        except ValueError:
            logger.error("Invalid JSON while polling interpretation result.")
            raise FetchingError("Invalid response format.") from None

        state = result.get("state")
        logger.debug("Interpretation poll state: %s", state)

        if state == "SUCCESS":
            logger.info("Interpretation completed for '%s'.", title_slug)
            return result

        time.sleep(0.10)
