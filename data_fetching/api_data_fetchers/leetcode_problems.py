import json
import requests

def fetch_leetcode_problems():
    API_URL = "https://leetcode.com/api/problems/algorithms/"

    try:
        response = requests.get(API_URL)
        response.raise_for_status()  # Raise an exception for HTTP errors

    except requests.RequestException as e:
        print(f"Error: Failed to fetch problems from LeetCode API. Details: {e}")
        return None

    try:
        data = response.json()

    except json.JSONDecodeError:
        print("Error: Failed to parse JSON response from LeetCode API.")
        return None

    # Initialize the list to hold problem details
    problems = []

    # Iterate over each problem entry in the response
    for pair in data.get("stat_status_pairs", []):
        stat = pair.get("stat", {})
        
        # Extract difficulty level and map it to string
        difficulty_level = pair.get("difficulty", {}).get("level", 0)
        
        # Extract passed_submissions and total_submissions
        passed_submissions = pair.get("stat", {}).get("total_acs", 0)
        total_submissions = pair.get("stat", {}).get("total_submitted", 0)
        
        problem = {
            "title": stat.get("question__title"),
            "title_slug": stat.get("question__title_slug"),
            "question_id": stat.get("question_id"),
            "is_paid_only": pair.get("paid_only", False),
            "difficulty": difficulty_level,
            "passed_submissions": passed_submissions,
            "total_submissions": total_submissions
        }

        problems.append(problem)

    print(f"Fetched {len(problems)} problems.")
    return problems
