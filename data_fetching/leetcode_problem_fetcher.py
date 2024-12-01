from ..data_fetching.graphql_queries import GRAPHQL_QUERIES, GRAPHQL_URL 

from ..user_utils import get_cookie, extract_csrf_token

import requests

class LeetCodeProblemFetcher:

    @staticmethod
    def fetch_problemset(tags=None, difficulty=None, limit=50, skip=0, category_slug="all-code-essentials"):
        if not category_slug:
            print("Error: category_slug is required but not provided.")
            return None

        if tags is not None and not isinstance(tags, list):
            print("Error: tags must be a list of strings.")
            return None

        if difficulty is not None and not (isinstance(difficulty, str) or (isinstance(difficulty, list) and all(isinstance(d, str) for d in difficulty))):
            print("Error: difficulty must be a string or a list of strings.")
            return None

        # Validate difficulty values
        valid_difficulties = {"EASY", "MEDIUM", "HARD"}
        difficulties = []
        if isinstance(difficulty, str):
            difficulties = [difficulty.upper()]

        elif isinstance(difficulty, list):
            difficulties = [d.upper() for d in difficulty]

        for d in difficulties:
            if d not in valid_difficulties:
                print(f"Error: Invalid difficulty level '{d}'. Valid options are EASY, MEDIUM, HARD.")
                return None

        query = GRAPHQL_QUERIES['problemset_data']

        payload = {
            "query": query,
            "variables": {
                "categorySlug": category_slug,
                "skip": skip,
                "limit": limit,
                "filters": {}
            },
            "operationName": "problemsetQuestionList"
        }

        # Add tags to filters if provided
        if tags:
            payload["variables"]["filters"]["tags"] = tags
            print("Tags filter applied:", tags)

        # Add difficulty to filters if provided
        if difficulties:
            if len(difficulties) == 1:
                payload["variables"]["filters"]["difficulty"] = difficulties[0]
            else:
                payload["variables"]["filters"]["difficulty"] = difficulties
            print("Difficulty filter applied:", difficulties)

        cookie = get_cookie()
        headers = None

        # TODO: Check if cookie is valid: cookie might be set but inactive
        try:
            if cookie:
                headers = {
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0",
                    "Cookie": cookie,
                    "x-csrftoken": extract_csrf_token(cookie),
                    "Referer": f"https://leetcode.com/problemset/",
                }

                response = requests.post(GRAPHQL_URL, json=payload, headers=headers)

            else:
                response = requests.post(GRAPHQL_URL, json=payload)
            
            if response.status_code == 200:
                result = response.json()

                if "errors" in result:
                    print(f"Error from API: {result['errors']}")
                    return None


                return result

            elif response.status_code == 401:
                print("Error: Unauthorized. Cookie might be invalid or expired.")

            else:
                print(f"Error: Failed to fetch problems. HTTP Status Code: {response.status_code}")

        except requests.RequestException as e:
            print(f"Error: Network or API issue occurred: {e}")

        return None

    @staticmethod
    def fetch_problem_data(title_slug):
        if not title_slug:
            print("Error: title_slug is required but not provided.")
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
            
            if response.status_code == 200:
                result = response.json()

                if "errors" in result:
                    print(f"Error from API: {result['errors']}")
                    return None

                return result

            elif response.status_code == 401:
                print("Error: Unauthorized. Cookie might be invalid or expired.")

            else:
                print(f"Error: Failed to fetch question details. HTTP Status Code: {response.status_code}")

        except requests.RequestException as e:
            print(f"Error: Network or API issue occurred: {e}")

        return None
