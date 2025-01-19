import logging
from typing import Dict, Any
from leetcode_cli.models.stats import UserStatsModel
from leetcode_cli.exceptions.exceptions import ParsingError

logger = logging.getLogger(__name__)


def parse_user_stats_data(json_data: Dict[str, Any]) -> UserStatsModel:
    """
    Parse the raw stats JSON into a UserStatsModel:
      - accepted/failed/untouched
      - beats: { 'EASY': x, 'MEDIUM': y, 'HARD': z }
    """
    try:
        user_progress = json_data["data"]["userProfileUserQuestionProgressV2"]

        accepted = {
            item["difficulty"].upper(): item["count"]
            for item in user_progress.get("numAcceptedQuestions", [])
        }
        failed = {
            item["difficulty"].upper(): item["count"]
            for item in user_progress.get("numFailedQuestions", [])
        }
        untouched = {
            item["difficulty"].upper(): item["count"]
            for item in user_progress.get("numUntouchedQuestions", [])
        }

        # Beats
        beats = {}
        for item in user_progress.get("userSessionBeatsPercentage", []):
            diff = item["difficulty"].upper()
            beats[diff] = float(item["percentage"])  # e.g. 72.3

        # Optional total submissions
        total_submissions = 0
        for diff in accepted:
            total_submissions += accepted[diff] + failed.get(diff, 0)

        return UserStatsModel(
            accepted=accepted,
            failed=failed,
            untouched=untouched,
            beats=beats,
            total_submissions=total_submissions,
        )

    except KeyError as e:
        logger.error(f"Missing key in stats data: {e}")
        raise ParsingError(f"Missing key in stats data: {e}")
    except TypeError as e:
        logger.error(f"Invalid structure in stats data: {e}")
        raise ParsingError(f"Invalid structure in stats data: {e}")


def parse_single_year_calendar(json_data: Dict[str, Any]) -> Dict[int, int]:
    """
    Parse the raw JSON for a single year's userCalendar submissionCalendar
    into a dict {timestamp: submissionCount}.
    """
    import json

    try:
        matched = json_data["data"]["matchedUser"]
        calendar_str = matched["userCalendar"]["submissionCalendar"]
    except (KeyError, TypeError) as e:
        logger.error(f"Missing or invalid calendar data: {e}")
        raise ParsingError(f"Missing or invalid calendar data: {e}")

    try:
        calendar_dict = json.loads(calendar_str)  # e.g. {"1620000000": 1, ...}
        return {int(k): v for k, v in calendar_dict.items()}
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding submissionCalendar JSON: {e}")
        raise ParsingError(f"Invalid submissionCalendar JSON: {e}")
