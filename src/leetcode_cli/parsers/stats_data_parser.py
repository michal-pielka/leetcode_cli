# file: leetcode_cli/parsers/stats_data_parser.py

import logging
from typing import Dict, Any
from leetcode_cli.models.stats import UserStatsModel
from leetcode_cli.exceptions.exceptions import ParsingError

logger = logging.getLogger(__name__)

def parse_user_stats_data(json_data: Dict[str, Any]) -> UserStatsModel:
    """
    Parse the raw stats JSON into a UserStatsModel (accepted/failed/untouched).
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
        return UserStatsModel(accepted=accepted, failed=failed, untouched=untouched)

    except KeyError as e:
        logger.error(f"Missing key in stats data: {e}")
        raise ParsingError(f"Missing key in stats data: {e}")

    except TypeError as e:
        logger.error(f"Invalid structure in stats data: {e}")
        raise ParsingError(f"Invalid structure in stats data: {e}")


def parse_single_year_calendar(json_data: Dict[str, Any]) -> Dict[int, int]:
    """
    Parse the raw JSON for a single year's userCalendar submissionCalendar
    into a dict {timestamp: submissionCount}, without join/fill logic.
    """
    try:
        matched = json_data["data"]["matchedUser"]
        calendar_str = matched["userCalendar"]["submissionCalendar"]  # e.g. "{\"1620000000\":1, ...}"
    except (KeyError, TypeError) as e:
        logger.error(f"Missing or invalid calendar data: {e}")
        raise ParsingError(f"Missing or invalid calendar data: {e}")

    import json
    try:
        calendar_dict = json.loads(calendar_str)  # { "1620000000": 1, ...}
        # Convert keys to int
        parsed_calendar = {int(k): v for k, v in calendar_dict.items()}
        return parsed_calendar
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding submissionCalendar JSON: {e}")
        raise ParsingError(f"Invalid submissionCalendar JSON: {e}")
