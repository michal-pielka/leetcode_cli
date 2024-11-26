from ..graphql_queries import GRAPHQL_QUERIES, GRAPHQL_URL

import requests

def fetch_leetcode_stats(user_slug):
    if not user_slug:
        print("Error: Username was not found in config file nor provided in this call.")
        return None

    url = GRAPHQL_URL

    payload = {
        "query": GRAPHQL_QUERIES['user_stats'],

        "variables": {
            "userSlug": user_slug
        },

        "operationName": "userProfileUserQuestionProgressV2"
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            result = response.json()

            if "errors" in result:
                print(f"Error from API: {result['errors']}")
                return None

            return result

        elif response.status_code == 401:
            print("Error: Unauthorized. Cookie might be invalid or expired.")

        else:
            print(f"Error: Failed to fetch stats. HTTP Status Code: {response.status_code}")
    except requests.RequestException as e:

        print(f"Error: Network or API issue occurred: {e}")

    return None

