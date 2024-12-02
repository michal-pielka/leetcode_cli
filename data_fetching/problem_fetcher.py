import requests
import logging

from .graphql_queries import GRAPHQL_QUERIES, GRAPHQL_URL

logger = logging.getLogger(__name__)

class ProblemDataFetchError(Exception):
    """Custom exception for problem data fetching errors."""
    pass

def fetch_problem_data(title_slug):
    """
    Fetches problem data for the given title_slug.

    Args:
        title_slug (str): The title slug of the problem.

    Returns:
        dict: The problem data.

    Raises:
        ProblemDataFetchError: If fetching fails.
    """
    if not title_slug:
        raise ProblemDataFetchError("title_slug is required but not provided.")

    query = GRAPHQL_QUERIES['problem_data']

    payload = {
        "query": query,
        "variables": {
            "titleSlug": title_slug
        },
        "operationName": "questionData"
    }

    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()
        result = response.json()

        if "errors" in result:
            raise ProblemDataFetchError(f"Error from API: {result['errors']}")

        return result

    except requests.exceptions.HTTPError as http_err:
        raise ProblemDataFetchError(f"HTTP error occurred: {http_err}")
    except requests.RequestException as e:
        raise ProblemDataFetchError(f"Network or API issue occurred: {e}")
