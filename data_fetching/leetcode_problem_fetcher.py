import requests
import logging

from ..data_fetching.graphql_queries import GRAPHQL_QUERIES, GRAPHQL_URL
from ..user_utils import get_cookie, extract_csrf_token

logger = logging.getLogger(__name__)

def fetch_problem_data(title_slug):
    if not title_slug:
        logger.error("title_slug is required but not provided.")
        return None

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
