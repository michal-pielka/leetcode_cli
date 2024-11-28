from ..graphql_data_fetchers.graphql_queries import GRAPHQL_QUERIES, GRAPHQL_URL 

from ...user_utils import load_cookie, extract_csrf_token

import requests

class LeetCodeProblemFetcher:

    @staticmethod
    def fetch_problemset(tags, limit=50, skip=0, category_slug="all-code-essentials"):
        if not category_slug:
            print("Error: category_slug is required but not provided.")
            return None

        if not isinstance(tags, list):
            print("Error: tags must be a list of strings.")
            return None


        payload = {
            "query": GRAPHQL_QUERIES['problems_by_tags'],
            "variables": {
                "categorySlug": category_slug,
                "skip": skip,
                "limit": limit,
                "filters": {}
            },
            "operationName": "problemsetQuestionList"
        }

        if tags:
            payload["variables"]["filters"]["tags"] = tags
            print("found tags")


        cookie = load_cookie()
        headers = None

        if cookie:
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0",
                "Cookie": cookie,
                "x-csrftoken": extract_csrf_token(cookie),
                "Referer": f"https://leetcode.com/problemset/",
            }


        try:
            if cookie:
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

        query = """
        query questionData($titleSlug: String!) {
          question(titleSlug: $titleSlug) {
            questionId
            title
            titleSlug
            content
            difficulty
            likes
            dislikes
            exampleTestcases
            topicTags {
              name
              slug
            }
            hints
            isPaidOnly
          }
        }
        """

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
