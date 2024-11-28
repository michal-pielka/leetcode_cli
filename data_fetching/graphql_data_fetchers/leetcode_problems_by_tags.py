# TODO: Implement this, current approach is slow as shit


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


def get_problem_tags(title_slug):
    GRAPHQL_URL = "https://leetcode.com/graphql/"
    query = """
    query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            topicTags {
                name
                slug
            }
        }
    }
    """

    payload = {
        "query": query,
        "variables": {"titleSlug": title_slug}
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "LeetCode CLI Tool"
    }

    try:
        response = requests.post(GRAPHQL_URL, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        tags = data.get("data", {}).get("question", {}).get("topicTags", [])
        return [tag.get("name") for tag in tags]
    except requests.RequestException as e:
        print(f"Error fetching tags for '{title_slug}': {e}")
    except json.JSONDecodeError:
        print(f"Error: Failed to parse JSON response for '{title_slug}'.")
    except KeyError:
        print(f"Error: Unexpected data structure for '{title_slug}'.")
    return []

def filter_problems_by_tags(problems, tags):
    if not problems:
        print("No problems available to filter.")
        return []

    if not tags:
        print("No tags provided for filtering.")
        return []

    # Convert tags to lowercase for case-insensitive matching
    tags = set(tag.lower() for tag in tags)

    matching_title_slugs = []

    total_problems = len(problems)
    for idx, problem in enumerate(problems, start=1):
        title_slug = problem.get("title_slug")
        if not title_slug:
            continue  # Skip if title_slug is missing

        # Fetch tags for the current problem
        problem_tags = get_problem_tags(title_slug)
        problem_tags_lower = set(tag.lower() for tag in problem_tags)

        # Check if any of the problem's tags match the input tags
        if tags.intersection(problem_tags_lower):
            matching_title_slugs.append(title_slug)

        # Optional: Display progress
        if idx % 100 == 0 or idx == total_problems:
            print(f"Processed {idx}/{total_problems} problems.")

    print(f"Found {len(matching_title_slugs)} problems matching tags {tags}.")
    return matching_title_slugs

# Example usage
if __name__ == "__main__":
    problems = fetch_leetcode_problems()

    if not problems:
        exit(1)  # Exit if fetching failed

    # Step 2: Define tags to filter by
    tags_to_filter = ["Array", "Dynamic Programming"]  # Example tags

    # Step 3: Filter problems by tags
    matching_slugs = filter_problems_by_tags(problems, tags_to_filter)

    # Step 4: Display the matching title_slugs
    print("\nProblems matching the specified tags:")
    for slug in matching_slugs:
        print(slug)

    # Optional: Save the matching slugs to a JSON file
    with open("filtered_problems.json", "w") as f:
        json.dump(matching_slugs, f, indent=4)
    print("\nMatching title_slugs have been saved to 'filtered_problems.json'.")
