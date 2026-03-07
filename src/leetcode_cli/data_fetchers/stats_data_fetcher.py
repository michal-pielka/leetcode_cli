import requests
import logging

from leetcode_cli.data_fetchers.graphql_queries import GRAPHQL_URL, GRAPHQL_QUERIES
from leetcode_cli.exceptions.exceptions import FetchingError

logger = logging.getLogger(__name__)


def fetch_user_stats(username):
    logger.info("Fetching stats for user '%s'.", username)
    query = GRAPHQL_QUERIES["user_problem_stats"]
    payload = {
        "query": query,
        "variables": {"userSlug": username},
        "operationName": "userProfileUserQuestionProgressV2",
    }

    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()
        result = response.json()

    except requests.RequestException as e:
        logger.error("Network error fetching stats for '%s': %s", username, e)
        raise FetchingError(
            f"Network error while fetching stats for user {username}: {e}"
        )

    except ValueError:
        logger.error("Invalid JSON response for stats of '%s'.", username)
        raise FetchingError("Failed to parse JSON response while fetching user stats.")

    logger.debug("Fetched stats for '%s' successfully.", username)
    return result


def fetch_user_activity(username, year):
    logger.info("Fetching activity for user '%s' in year %s.", username, year)
    query = GRAPHQL_QUERIES["user_calendar"]
    payload = {
        "query": query,
        "variables": {"username": username, "year": year},
        "operationName": "userProfileCalendar",
    }

    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()
        result = response.json()

    except requests.RequestException as e:
        logger.error(
            "Network error fetching activity for '%s' in %s: %s", username, year, e
        )
        raise FetchingError(
            f"Network error while fetching user activity for {username} in {year}: {e}"
        )

    except ValueError:
        logger.error("Invalid JSON response for activity of '%s' in %s.", username, year)
        raise FetchingError(
            "Failed to parse JSON response while fetching user activity."
        )

    logger.debug("Fetched activity for '%s' in %s successfully.", username, year)
    return result
