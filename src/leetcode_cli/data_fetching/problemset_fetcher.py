import requests
import logging


from leetcode_cli.data_fetching.graphql_queries import GRAPHQL_QUERIES, GRAPHQL_URL

logger = logging.getLogger(__name__)


def fetch_problemset(cookie=None, csrf_token=None, tags=None, difficulty=None, limit=50, skip=0, category_slug="all-code-essentials"):
    # Validate difficulty values
    valid_difficulties = {None, "EASY", "MEDIUM", "HARD"}

    if difficulty not in valid_difficulties:
        logger.error(f"Invalid difficulty level '{difficulty}'. Valid options are EASY, MEDIUM, HARD.")
        return None

    query = GRAPHQL_QUERIES['problemset_data']

    payload = {
        "query": query,
        "variables": {
            "categorySlug": category_slug,
            "skip": skip,
            "limit": limit,
            "filters": {}
        },
        "operationName": "problemsetQuestionList"
    }

    # Add tags to filters if provided
    if tags:
        payload["variables"]["filters"]["tags"] = tags
        logger.debug(f"Tags filter applied: {tags}")

    # Add difficulty to filters if provided
    if difficulty:
        payload["variables"]["filters"]["difficulty"] = difficulty

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
    }

    # If cookie and csrf_token are set, add to headers
    if cookie and csrf_token:
        headers["Cookie"] = cookie
        headers["x-csrftoken"] = csrf_token 
        headers["Referer"] = f"https://leetcode.com/problemset/"

    response = requests.post(GRAPHQL_URL, json=payload, headers=headers)
    result = response.json()

    if response.status_code != 200:
        return {}

    return result.get("data", {}).get("problemsetQuestionList", {}).get("questions", {})

