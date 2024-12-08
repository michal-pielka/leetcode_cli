
# leetcode_cli/parsers/stats_parser.py
import logging
from typing import Dict, Any
from leetcode_cli.models.stats import UserStatsModel, UserActivityModel
from leetcode_cli.utils.stats_utils import (
    join_and_slice_calendars,
    fill_daily_activity
)
from leetcode_cli.exceptions.exceptions import ParsingError

logger = logging.getLogger(__name__)

def parse_user_stats_data(json_data: Dict[str, Any]) -> UserStatsModel:
    """
    Parse the raw stats JSON data into a UserStatsModel.
    """
    try:
        user_progress = json_data["data"]["userProfileUserQuestionProgressV2"]
        accepted = {item["difficulty"].upper(): item["count"] for item in user_progress.get("numAcceptedQuestions", [])}
        failed = {item["difficulty"].upper(): item["count"] for item in user_progress.get("numFailedQuestions", [])}
        untouched = {item["difficulty"].upper(): item["count"] for item in user_progress.get("numUntouchedQuestions", [])}

        return UserStatsModel(accepted=accepted, failed=failed, untouched=untouched)
    except KeyError as e:
        logger.error(f"Missing key in stats data: {e}")
        raise ParsingError(f"Missing key in stats data: {e}")
    except TypeError as e:
        logger.error(f"Invalid structure in stats data: {e}")
        raise ParsingError(f"Invalid structure in stats data: {e}")

def parse_user_activity_data(previous_year_data: Dict[str, Any], current_year_data: Dict[str, Any]) -> UserActivityModel:
    """
    Parse the raw calendar activity data from two years into a UserActivityModel.
    This involves joining, slicing, and filling the daily activity dictionary.
    """
    try:
        joined_activity = join_and_slice_calendars(previous_year_data, current_year_data)
        filled_activity = fill_daily_activity(joined_activity)
        return UserActivityModel(daily_activity=filled_activity)
    except Exception as e:
        logger.error(f"Error parsing user activity data: {e}")
        raise ParsingError(f"Error parsing user activity data: {e}")
