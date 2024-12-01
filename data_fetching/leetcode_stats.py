from ..data_fetching.graphql_queries import GRAPHQL_QUERIES, GRAPHQL_URL

import requests

def fetch_leetcode_stats(username):
    if not username:
        print("Error: Username was not provided")
        return None

    payload = {
        "query": GRAPHQL_QUERIES['problem_stats'],

        "variables": {
            "userSlug": username
        },

        "operationName": "userProfileUserQuestionProgressV2"
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
            print(f"Error: Failed to fetch stats. HTTP Status Code: {response.status_code}")
    except requests.RequestException as e:

        print(f"Error: Network or API issue occurred: {e}")

    return None


def fetch_leetcode_activity(username, year):
    if not username:
        print("Error: Username was not provided")
        return None


    if year is None:
        print("Error: year is None")
        return None

    payload = {
        "query": GRAPHQL_QUERIES['user_calendar'],
        "variables": {
            "username": username,
            "year": year
        },
        "operationName": "userProfileCalendar"
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
            print(f"Error: Failed to fetch activity data. HTTP Status Code: {response.status_code}")

    except requests.RequestException as e:
        print(f"Error: Network or API issue occurred: {e}")

    return None

