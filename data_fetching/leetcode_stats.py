import requests
import logging

from ..data_fetching.graphql_queries import GRAPHQL_QUERIES, GRAPHQL_URL

logger = logging.getLogger(__name__)


def fetch_leetcode_stats(username):
    if not username:
        logger.error("Username was not provided")
        return None

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


def fetch_leetcode_activity(username, year):
    if not username:
        logger.error("Username was not provided")
        return None

    if year is None:
        logger.error("Year is None")
        return None

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
