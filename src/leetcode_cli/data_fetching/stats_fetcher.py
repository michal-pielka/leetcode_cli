import requests
import logging

from leetcode_cli.data_fetching.graphql_queries import GRAPHQL_URL, GRAPHQL_QUERIES

logger = logging.getLogger(__name__)

class LeetCodeStatsFetchError(Exception):
    """Custom exception for LeetCode stats fetching errors."""
    pass

def fetch_user_stats(username):
    """
    Fetches LeetCode stats for the given username.

    Args:
        username (str): The username.

    Returns:
        dict: The stats data.

    Raises:
        LeetCodeStatsFetchError: If fetching fails.
    """
    if not username:
        raise LeetCodeStatsFetchError("Username was not provided.")

    query = GRAPHQL_QUERIES['problem_stats']

    payload = {
        "query": query,
        "variables": {
            "userSlug": username
        },
        "operationName": "userProfileUserQuestionProgressV2"
    }

    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()
        result = response.json()

        if "errors" in result:
            raise LeetCodeStatsFetchError(f"Error from API: {result['errors']}")

        return result

    except requests.exceptions.HTTPError as http_err:
        raise LeetCodeStatsFetchError(f"HTTP error occurred: {http_err}")
    except requests.RequestException as e:
        raise LeetCodeStatsFetchError(f"Network or API issue occurred: {e}")

def fetch_user_activity(username, year):
    """
    Fetches LeetCode activity calendar for the given username and year.

    Args:
        username (str): The username.
        year (int): The year.

    Returns:
        dict: The activity data.

    Raises:
        LeetCodeStatsFetchError: If fetching fails.
    """
    if not username:
        raise LeetCodeStatsFetchError("Username was not provided.")

    if year is None:
        raise LeetCodeStatsFetchError("Year is None.")

    query = GRAPHQL_QUERIES['user_calendar']

    payload = {
        "query": query,
        "variables": {
            "username": username,
            "year": year
        },
        "operationName": "userProfileCalendar"
    }

    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()
        result = response.json()

        if "errors" in result:
            raise LeetCodeStatsFetchError(f"Error from API: {result['errors']}")

        return result

    except requests.exceptions.HTTPError as http_err:
        raise LeetCodeStatsFetchError(f"HTTP error occurred: {http_err}")
    except requests.RequestException as e:
        raise LeetCodeStatsFetchError(f"Network or API issue occurred: {e}")
