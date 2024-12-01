import requests
import json

from ..data_fetching.graphql_queries import GRAPHQL_URL, GRAPHQL_QUERIES

# TODO: Implement code snippet builder for each language, so it doesn't waste time doing request

def fetch_code_snippet(title_slug, lang_slug):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }

    variables = {
        "titleSlug": title_slug
    }

    payload = {
        "query": GRAPHQL_QUERIES["code_snippets"],
        "variables": variables
    }

    try:
        response = requests.post(GRAPHQL_URL, headers=headers, data=json.dumps(payload))

    except requests.RequestException as e:
        raise ConnectionError(f"An error occurred while making the request: {e}")

    if response.status_code != 200:
        raise ConnectionError(f"Failed to fetch data from API. Status code: {response.status_code}")

    try:
        data = response.json()
    except json.JSONDecodeError:
        raise ValueError("Response content is not valid JSON.")

    try:
        code_snippets = data['data']['question']['codeSnippets']
    except KeyError:
        raise ValueError("Unexpected JSON structure received from API.")

    # Search for the code snippet in the desired language
    for snippet in code_snippets:
        if snippet['langSlug'].lower() == lang_slug.lower():
            return snippet['code']

    # If code snippet is not found
    raise ValueError(f"No code snippet found for language slug: '{lang_slug}'")
