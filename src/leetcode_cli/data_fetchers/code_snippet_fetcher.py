import logging

import requests

from leetcode_cli.data_fetchers.graphql_queries import GRAPHQL_QUERIES, GRAPHQL_URL
from leetcode_cli.exceptions.exceptions import FetchingError

logger = logging.getLogger(__name__)


def fetch_code_snippet(title_slug, lang_slug):
    logger.info("Fetching code snippet for '%s' in '%s'.", title_slug, lang_slug)
    query = GRAPHQL_QUERIES["code_snippets"]
    payload = {"query": query, "variables": {"titleSlug": title_slug}}

    try:
        response = requests.post(GRAPHQL_URL, json=payload)
        response.raise_for_status()
        result = response.json()

    except requests.RequestException as e:
        logger.error(
            "Network error fetching code snippet for '%s' in '%s': %s",
            title_slug,
            lang_slug,
            e,
        )
        raise FetchingError(f"Network error while fetching code snippet for {title_slug} in {lang_slug}: {e}") from e

    except ValueError:
        logger.error("Invalid JSON response for code snippet of '%s'.", title_slug)
        raise FetchingError("Failed to parse JSON response while fetching code snippet.") from None

    logger.debug("Fetched code snippet for '%s' in '%s' successfully.", title_slug, lang_slug)
    return result
