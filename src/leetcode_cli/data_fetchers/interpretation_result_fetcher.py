import requests
import time
from typing import Dict
from leetcode_cli.exceptions.exceptions import FetchingError
from leetcode_cli.services.problemset_service import load_problemset_metadata, get_problem_by_key_value
from leetcode_cli.data_fetchers.problem_data_fetcher import fetch_problem_id


def fetch_interpretation_result(cookie: str, csrf_token: str, title_slug: str, code: str, language: str, testcases: str) -> Dict:
    """
    Fetch the 'Run Code' / interpretation result from LeetCode for a given problem.
    """
    problems_data = load_problemset_metadata()
    if not problems_data:
        question_id = fetch_problem_id(title_slug).get("data", {}).get("question", {}).get("questionId", None)
        if not question_id:
            raise FetchingError(f"Unable to find questionId for {title_slug}")

    else:
        question_data = get_problem_by_key_value(problems_data, "titleSlug", title_slug)
        if not question_data or "questionId" not in question_data:
            raise FetchingError(f"Unable to find questionId for {title_slug}")

        question_id = question_data["questionId"]

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

    try:
        response = requests.post(submit_url, json=payload, headers=headers)
        response.raise_for_status()
        submission = response.json()

    except requests.RequestException as e:
        raise FetchingError(f"Submission failed: {e}")

    except ValueError:
        raise FetchingError("Invalid response format from LeetCode.")

    interpret_id = submission.get('interpret_id')
    if not interpret_id:
        raise FetchingError("Interpretation ID not received.")

    # Check interpretation status until complete
    check_submission_url = f"https://leetcode.com/submissions/detail/{interpret_id}/check/"
    while True:
        try:
            r = requests.get(check_submission_url, headers=headers)
            r.raise_for_status()
            result = r.json()

        except requests.RequestException as e:
            raise FetchingError(f"Failed to check interpretation: {e}")

        except ValueError:
            raise FetchingError("Invalid response format.")

        if result.get('state') == "SUCCESS":
            return result

        time.sleep(0.10)
