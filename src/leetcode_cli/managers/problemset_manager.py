import logging
import os
import json
from typing import Dict, Any, Optional, List
import random

from leetcode_cli.managers.auth_service import AuthService
from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.exceptions.exceptions import ProblemSetError

from leetcode_cli.data_fetchers.problemset_data_fetcher import fetch_problemset
from leetcode_cli.parsers.problemset_data_parser import parse_problemset_data

logger = logging.getLogger(__name__)


class ProblemSetManager:
    """
    Manages problem set-related functionalities, including loading and saving problem metadata.
    """

    def __init__(self, config_manager: ConfigManager, auth_service: AuthService):
        self.config_manager = config_manager
        self.auth_service = auth_service
        self.problems_data_path = self.get_problems_data_path()

    #
    # ──────────────────────────────────────────────────────
    #   PUBLIC METHODS
    # ──────────────────────────────────────────────────────
    #

    def get_problemset(self, tags=None, difficulty=None, limit=50, page=1):
        """
        High-level method to fetch problemset from the GraphQL API,
        parse it, and return the structured result.
        """
        try:
            raw = fetch_problemset(
                cookie=self.auth_service.get_cookie(),
                csrf_token=self.auth_service.get_csrf_token(),
                tags=tags,
                difficulty=difficulty,
                limit=limit,
                skip=(page - 1) * limit
            )

        except Exception as e:
            logger.error(e)
            raise e

        try:
            parsed = parse_problemset_data(raw)
            return parsed

        except ProblemSetError as e:
            logger.error(e)
            raise e


    def load_problemset_metadata(self) -> Dict[str, Any]:
        """
        Loads the local JSON file that caches problem set data.

        Returns:
            Dict[str, Any]: The loaded problem set metadata.

        Raises:
            ProblemSetError: If the file cannot be read or is corrupted.
        """
        if os.path.exists(self.problems_data_path):
            try:
                with open(self.problems_data_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    logger.debug("Loaded problem set metadata successfully.")
                    return data

            except json.JSONDecodeError as e:
                logger.error(f"problems_metadata.json is corrupted: {e}")
                raise ProblemSetError("problems_metadata.json is corrupted.")

            except OSError as e:
                logger.error(f"Failed to read problems_metadata.json: {e}")
                raise ProblemSetError("Failed to read problems_metadata.json.")

        else:
            logger.warning(f"problems_metadata.json not found at '{self.problems_data_path}'.")
            return {}

    def save_problemset_metadata(self, data: Dict[str, Any]) -> None:
        """
        Saves the problem set metadata to the local JSON file.

        Args:
            data (Dict[str, Any]): The problem set data to save.

        Raises:
            ProblemSetError: If the file cannot be written.
        """
        try:
            os.makedirs(os.path.dirname(self.problems_data_path), exist_ok=True)

            with open(self.problems_data_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

            logger.info(f"Problem set data saved to '{self.problems_data_path}'.")

        except OSError as e:
            logger.error(f"Failed to save problems_metadata.json: {e}")
            raise ProblemSetError("Failed to save problems_metadata.json.")

    def get_problem_by_key_value(self, key: str, value: str) -> Dict[str, Any]:
        """
        Retrieves a problem from the problem set based on a key-value pair.

        Args:
            key (str): The key to search by (e.g., 'frontendQuestionId', 'titleSlug').
            value (str): The value to match.

        Returns:
            Dict[str, Any]: The matched problem data.

        Raises:
            ProblemSetError: If the problem cannot be found.
        """
        problems_data = self.load_problemset_metadata()
        questions = problems_data.get('data', {}).get('problemsetQuestionList', {}).get('questions', [])

        for problem in questions:
            if str(problem.get(key, "")).lower() == str(value).lower():
                logger.debug(f"Found problem with {key}='{value}'.")
                return problem

        logger.warning(f"Problem with {key}='{value}' not found in cached data.")
        return {}

    def get_random_local_problem_slug(self, difficulty: Optional[str], tags: Optional[List[str]]) -> Optional[str]:
        """
        Randomly select a local problem that matches the given difficulty and tag filters.
        Returns its 'titleSlug', or None if no match found.
        """
        data = self.load_problemset_metadata()
        questions = data.get('data', {}).get('problemsetQuestionList', {}).get('questions', [])

        # Filter by difficulty & tags if provided
        filtered = []
        for q in questions:
            if difficulty and q.get("difficulty", "").lower() != difficulty.lower():
                continue

            if tags and not self._matches_tags(q, tags):
                continue

            filtered.append(q)

        if not filtered:
            return None

        # Randomly choose one from the filtered list
        chosen = random.choice(filtered)
        return chosen.get("titleSlug")
    
    def get_problems_data_path(self) -> str:
        """
        Construct the path to problems_metadata.json in config_dir.
        """
        config_dir = self.config_manager.config_dir
        return os.path.join(config_dir, "problems_metadata.json")

    #
    # ──────────────────────────────────────────────────────
    #   PRIVATE HELPERS
    # ──────────────────────────────────────────────────────
    #

    def _matches_tags(self, question: dict, required_tags: List[str]) -> bool:
        """
        Helper to check if the question has all the required tags.
        'topicTags' is typically a list of dicts with 'slug' keys.
        """
        question_tags = [t.get("slug", "").lower() for t in question.get("topicTags", [])]

        for required_tag in required_tags:
            if required_tag.lower() not in question_tags:
                return False

        return True
