import requests
import logging

from leetcode_cli.data_fetching.graphql_queries import GRAPHQL_URL, GRAPHQL_QUERIES

logger = logging.getLogger(__name__)

class CodeSnippetFetchError(Exception):
    """Custom exception for code snippet fetching errors."""
    pass

def fetch_code_snippet(title_slug, lang_slug):
    """
    Fetches the code snippet for a given problem and language.

    Args:
        title_slug (str): The title slug of the problem.
        lang_slug (str): The language slug (e.g., 'python', 'cpp').

    Returns:
        str: The code snippet in the specified language.

    Raises:
        CodeSnippetFetchError: If fetching fails or the snippet is not found.
    """
    query = GRAPHQL_QUERIES["code_snippets"]

    payload = {
        "query": query,
        "variables": {
            "titleSlug": title_slug
        }
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.post(GRAPHQL_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        logger.error(f"Failed to fetch code snippet: {e}")
        raise CodeSnippetFetchError(f"Failed to fetch code snippet: {e}")

    try:
        code_snippets = data['data']['question']['codeSnippets']
    except KeyError:
        logger.error("Invalid response structure when fetching code snippet.")
        raise CodeSnippetFetchError("Invalid response structure.")

    available_lang_slugs = []
    for snippet in code_snippets:
        if snippet['langSlug'].lower() == lang_slug.lower():
            return snippet['code']
        else:
            available_lang_slugs.append(snippet['langSlug'].lower())

    raise CodeSnippetFetchError(f"No code snippet found for language slug: '{lang_slug}', available slugs: {" ,".join(available_lang_slugs)}")
