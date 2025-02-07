import requests
import logging

from leetcode_cli.data_fetchers.graphql_queries import GRAPHQL_QUERIES, GRAPHQL_URL
from leetcode_cli.exceptions.exceptions import FetchingError

logger = logging.getLogger(__name__)


def fetch_problemset(
    cookie=None, csrf_token=None, tags=None, difficulty=None, limit=50, skip=0
):
    query = GRAPHQL_QUERIES["problemset_data"]
    payload = {
        "query": query,
        "variables": {
            "categorySlug": "all-code-essentials",
            "skip": skip,
            "limit": limit,
            "filters": {},
        },
        "operationName": "problemsetQuestionList",
    }

    if tags:
        payload["variables"]["filters"]["tags"] = tags

    if difficulty:
        payload["variables"]["filters"]["difficulty"] = difficulty

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
    }

    if cookie and csrf_token:
        headers["Cookie"] = cookie
        headers["x-csrftoken"] = csrf_token
        headers["Referer"] = "https://leetcode.com/problemset/"

    try:
        response = requests.post(GRAPHQL_URL, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

    except requests.RequestException as e:
        raise FetchingError(f"Network error while fetching problemset: {e}")

    except ValueError:
        raise FetchingError(
            "Failed to parse JSON response while fetching problemset, there might be an issue with your cookie."
        )

    return result


def fetch_problemset_metadata():
    query = GRAPHQL_QUERIES["problemset_metadata"]
    payload = {
        "query": query,
        "variables": {
            "categorySlug": "all-code-essentials",
            "skip": 0,
            "limit": 10000000,
            "filters": {},
        },
        "operationName": "problemsetQuestionList",
    }

    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()
        result = response.json()

    except requests.RequestException as e:
        raise FetchingError(f"Network error while fetching problemset: {e}")

    except ValueError:
        raise FetchingError("Failed to parse JSON response while fetching problemset.")

    return result
