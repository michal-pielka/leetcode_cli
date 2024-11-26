def parse_leetcode_stats(data, user_slug):
    rectangles_total = 20
    filled_char = "█"
    empty_char = "░"

    # Define ANSI escape sequences for colors
    difficulty_colors = {
        "EASY": "\033[32m",  # Green
        "MEDIUM": "\033[33m",  # Yellow (close to orange)
        "HARD": "\033[31m"   # Red
    }
    reset_color = "\033[0m"  # Reset color

    try:
        progress = data["data"]["userProfileUserQuestionProgressV2"]

        # Extract data
        num_accepted = {item["difficulty"]: item["count"] for item in progress["numAcceptedQuestions"]}
        total_questions = {
            item["difficulty"]: item["count"] + sum(
                other["count"] for other in progress["numFailedQuestions"] + progress["numUntouchedQuestions"]
                if other["difficulty"] == item["difficulty"]
            )
            for item in progress["numAcceptedQuestions"]
        }
        beats_percentage = {item["difficulty"]: item["percentage"] for item in progress["userSessionBeatsPercentage"]}

        difficulties = ["EASY", "MEDIUM", "HARD"]

        # Build formatted output
        result = []
        for difficulty in difficulties:
            # Data
            passed = num_accepted.get(difficulty, 0)
            total = total_questions.get(difficulty, 0)
            percentage = beats_percentage.get(difficulty, 0.0)

            # Rectangles
            filled = round((passed / total) * rectangles_total) if total > 0 else 0
            filled = min(max(filled, 0), rectangles_total)  # Ensure within bounds
            bar = filled_char * filled + empty_char * (rectangles_total - filled)

            # Formatting
            color = difficulty_colors.get(difficulty, reset_color)
            diff_formatted = f"{difficulty:<6}"  # Left-align and pad to 6 characters
            passed_formatted = f"{passed:>4}"
            total_formatted = f"{total:<4}"
            percentage_formatted = f"{percentage:.2f}%"

            result.append(
                f"{color}{diff_formatted} {passed_formatted}/{total_formatted} {bar} beats {percentage_formatted}{reset_color}"
            )

        return f"LeetCode Stats for {user_slug}\n" + "\n".join(result)

    except (KeyError, TypeError, ZeroDivisionError) as e:
        print(f"Error: Unexpected data format from LeetCode. Details: {e}")
        return None

# -------------------- Example Usage -------------------- #
from ..graphql.data_fetchers.leetcode_stats import fetch_leetcode_stats

if __name__ == "__main__":
    stats_data = fetch_leetcode_stats("BucketAbuser")
    if stats_data:
        formatted_stats = parse_leetcode_stats(stats_data, "BucketAbuser")
        if formatted_stats:
            print(formatted_stats)
