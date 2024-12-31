import requests
import logging

from leetcode_cli.data_fetching.graphql_queries import GRAPHQL_URL, GRAPHQL_QUERIES
from leetcode_cli.exceptions.exceptions import FetchingError

logger = logging.getLogger(__name__)

def fetch_user_stats(username):
    query = GRAPHQL_QUERIES['user_problem_stats']

    payload = {
        "query": query,
        "variables": {"userSlug": username},
        "operationName": "userProfileUserQuestionProgressV2"
    }

    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()
        result = response.json()

    except requests.RequestException as e:
        raise FetchingError(f"Network error while fetching stats for user {username}: {e}")

    except ValueError:
        raise FetchingError("Failed to parse JSON response while fetching user stats.")

    return result

def fetch_user_activity(username, year):
    query = GRAPHQL_QUERIES['user_calendar']
    
    payload = {
        "query": query,
        "variables": {"username": username, "year": year},
        "operationName": "userProfileCalendar"
    }

    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()
        result = response.json()

    except requests.RequestException as e:
        raise FetchingError(f"Network error while fetching user activity for {username} in {year}: {e}")

    except ValueError:
        raise FetchingError("Failed to parse JSON response while fetching user activity.")

    return result
