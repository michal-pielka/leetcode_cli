import requests
import logging
from leetcode_cli.data_fetchers.graphql_queries import GRAPHQL_URL, GRAPHQL_QUERIES
from leetcode_cli.exceptions.exceptions import FetchingError

logger = logging.getLogger(__name__)

def fetch_problem_testcases(title_slug):
    query = GRAPHQL_QUERIES['problem_testcases']
    payload = {
        "query": query,
        "variables": {"titleSlug": title_slug},
        "operationName": "questionData"
    }

    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
    except requests.RequestException as e:
        raise FetchingError(f"Network error while fetching testcases for {title_slug}: {e}")

    except ValueError:
        raise FetchingError("Failed to parse JSON response while fetching problem testcases.")

    return result

def fetch_problem_id(title_slug):
    query = GRAPHQL_QUERIES["problem_id"]
    payload = {
        "query": query,
        "variables": {"titleSlug": title_slug},
        "operationName": "questionDetail"
    }

    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()
        result = response.json()

    except requests.RequestException as e:
        raise FetchingError(f"Network error while fetching problem ID for {title_slug}: {e}")

    except ValueError:
        raise FetchingError("Failed to parse JSON response while fetching problem ID.")

    return result

def fetch_problem_frontend_id(title_slug):
    query = GRAPHQL_QUERIES["problem_frontend_id"]
    payload = {
        "query": query,
        "variables": {"titleSlug": title_slug},
        "operationName": "questionDetail"
    }

    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()
        result = response.json()

    except requests.RequestException as e:
        raise FetchingError(f"Network error while fetching problem ID for {title_slug}: {e}")

    except ValueError:
        raise FetchingError("Failed to parse JSON response while fetching problem ID.")

    return result

def fetch_random_title_slug(difficulty, tags):
    query = GRAPHQL_QUERIES["random_title_slug"]
    payload = {
        "query": query,
        "variables": {
            "categorySlug": "all-code-essentials",
            "filters": {}
        },
        "operationName": "randomQuestion"
    }

    if difficulty:
        payload["variables"]["filters"]["difficulty"] = difficulty

    if tags:
        payload["variables"]["filters"]["tags"] = tags

    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()
        result = response.json()

    except requests.RequestException as e:
        raise FetchingError(f"Netword error while fetching random title slug: {e}")

    except ValueError:
        raise FetchingError("Failed to parse JSON response while fetching random title slug.")

    return result

def fetch_problem_data(title_slug):
    query = GRAPHQL_QUERIES["problem_detail"]
    payload = {
        "query": query,
        "variables": {"titleSlug": title_slug},
        "operationName": "questionDetail"
    }

    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()
        result = response.json()

    except requests.RequestException as e:
        raise FetchingError(f"Network error while fetching problem data for {title_slug}: {e}")

    except ValueError:
        raise FetchingError("Failed to parse JSON response while fetching problem data.")

    return result
