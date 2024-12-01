import requests
import logging

from ..data_fetching.graphql_queries import GRAPHQL_URL, GRAPHQL_QUERIES

logger = logging.getLogger(__name__)

def fetch_code_snippet(title_slug, lang_slug):
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

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return None
    except requests.RequestException as e:
        logger.error(f"Network or API issue occurred: {e}")
        return None

    try:
        data = response.json()
    except ValueError:
        logger.error("Response content is not valid JSON.")
        return None

    try:
        code_snippets = data['data']['question']['codeSnippets']
        question_id = data['data']['question']['questionId']
        title_slug = data['data']['question']['titleSlug']
    except KeyError:
        logger.error("Unexpected JSON structure received from API.")
        return None

    # Search for the code snippet in the desired language
    for snippet in code_snippets:
        if snippet['langSlug'].lower() == lang_slug.lower():
            return {"code_snippet" : snippet['code'], "question_id" : question_id, "title_slug" : title_slug}

    # If code snippet is not found
    logger.error(f"No code snippet found for language slug: '{lang_slug}'")
    return None
