import logging

import requests

from leetcode_cli.data_fetchers.graphql_queries import GRAPHQL_QUERIES, GRAPHQL_URL
from leetcode_cli.exceptions.exceptions import FetchingError

logger = logging.getLogger(__name__)


def fetch_problem_testcases(title_slug):
    logger.info("Fetching testcases for '%s'.", title_slug)
    query = GRAPHQL_QUERIES["problem_testcases"]
    payload = {
        "query": query,
        "variables": {"titleSlug": title_slug},
        "operationName": "questionData",
    }

    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()
        result = response.json()

    except requests.RequestException as e:
        logger.error("Network error fetching testcases for '%s': %s", title_slug, e)
        raise FetchingError(f"Network error while fetching testcases for {title_slug}: {e}") from e

    except ValueError:
        logger.error("Invalid JSON response for testcases of '%s'.", title_slug)
        raise FetchingError("Failed to parse JSON response while fetching problem testcases.") from None

    logger.debug("Fetched testcases for '%s' successfully.", title_slug)
    return result


def fetch_problem_id(title_slug):
    logger.info("Fetching problem ID for '%s'.", title_slug)
    query = GRAPHQL_QUERIES["problem_id"]
    payload = {
        "query": query,
        "variables": {"titleSlug": title_slug},
        "operationName": "questionDetail",
    }

    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()
        result = response.json()

    except requests.RequestException as e:
        logger.error("Network error fetching problem ID for '%s': %s", title_slug, e)
        raise FetchingError(f"Network error while fetching problem ID for {title_slug}: {e}") from e

    except ValueError:
        logger.error("Invalid JSON response for problem ID of '%s'.", title_slug)
        raise FetchingError("Failed to parse JSON response while fetching problem ID.") from None

    logger.debug("Fetched problem ID for '%s' successfully.", title_slug)
    return result


def fetch_problem_frontend_id(title_slug):
    logger.info("Fetching frontend ID for '%s'.", title_slug)
    query = GRAPHQL_QUERIES["problem_frontend_id"]
    payload = {
        "query": query,
        "variables": {"titleSlug": title_slug},
        "operationName": "questionDetail",
    }

    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()
        result = response.json()

    except requests.RequestException as e:
        logger.error("Network error fetching frontend ID for '%s': %s", title_slug, e)
        raise FetchingError(f"Network error while fetching problem ID for {title_slug}: {e}") from e

    except ValueError:
        logger.error("Invalid JSON response for frontend ID of '%s'.", title_slug)
        raise FetchingError("Failed to parse JSON response while fetching problem ID.") from None

    logger.debug("Fetched frontend ID for '%s' successfully.", title_slug)
    return result


def fetch_random_title_slug(difficulty, tags):
    logger.info("Fetching random title slug (difficulty=%s, tags=%s).", difficulty, tags)
    query = GRAPHQL_QUERIES["random_title_slug"]
    payload = {
        "query": query,
        "variables": {"categorySlug": "all-code-essentials", "filters": {}},
        "operationName": "randomQuestion",
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
        logger.error("Network error fetching random title slug: %s", e)
        raise FetchingError(f"Network error while fetching random title slug: {e}") from e

    except ValueError:
        logger.error("Invalid JSON response for random title slug.")
        raise FetchingError("Failed to parse JSON response while fetching random title slug.") from None

    logger.debug("Fetched random title slug successfully.")
    return result


def fetch_problem_data(title_slug):
    logger.info("Fetching problem data for '%s'.", title_slug)
    query = GRAPHQL_QUERIES["problem_detail"]
    payload = {
        "query": query,
        "variables": {"titleSlug": title_slug},
        "operationName": "questionDetail",
    }

    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()
        result = response.json()

    except requests.RequestException as e:
        logger.error("Network error fetching problem data for '%s': %s", title_slug, e)
        raise FetchingError(f"Network error while fetching problem data for {title_slug}: {e}") from e

    except ValueError:
        logger.error("Invalid JSON response for problem data of '%s'.", title_slug)
        raise FetchingError("Failed to parse JSON response while fetching problem data.") from None

    logger.debug("Fetched problem data for '%s' successfully.", title_slug)
    return result
