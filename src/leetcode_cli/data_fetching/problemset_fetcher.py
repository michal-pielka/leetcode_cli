import requests
import logging


from ..data_fetching.graphql_queries import GRAPHQL_QUERIES, GRAPHQL_URL

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

    try:
        response = requests.post(GRAPHQL_URL, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

        if "errors" in result:
            logger.error(f"Error from API: {result['errors']}")
            return None

        return result

    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 401:
            logger.error("Unauthorized. Cookie might be invalid or expired.")
        else:
            logger.error(f"HTTP error occurred: {http_err}")
    except requests.RequestException as e:
        logger.error(f"Network or API issue occurred: {e}")

    return None
