import requests
import logging

from leetcode_cli.data_fetchers.graphql_queries import GRAPHQL_URL, GRAPHQL_QUERIES
from leetcode_cli.exceptions.exceptions import FetchingError

logger = logging.getLogger(__name__)

def fetch_code_snippet(title_slug, lang_slug):
    query = GRAPHQL_QUERIES["code_snippets"]
    payload = {
        "query": query,
        "variables": {"titleSlug": title_slug}
    }

    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()
        result = response.json()

    except requests.RequestException as e:
        raise FetchingError(f"Network error while fetching code snippet for {title_slug} in {lang_slug}: {e}")

    except ValueError:
        raise FetchingError("Failed to parse JSON response while fetching code snippet.")

    return result
