import logging
import os
import json
from typing import Dict, Any, Optional, Tuple

from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.exceptions.exceptions import ProblemSetError

logger = logging.getLogger(__name__)


class ProblemSetManager:
    """
    Manages problem set-related functionalities, including loading and saving problem metadata.
    """

    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.problems_data_path = self.get_problems_data_path()

    def get_problems_data_path(self) -> str:
        """
        Returns the path to the problems_metadata.json file.
        """
        config_dir = self.config_manager.config_dir
        return os.path.join(config_dir, "problems_metadata.json")

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

    def get_title_slug(self, frontend_question_id: str) -> Optional[str]:
        """
        Retrieves the title slug for a given frontend question ID.

        Args:
            frontend_question_id (str): The frontend question ID.

        Returns:
            Optional[str]: The title slug if found, else None.
        """
        problem = self.get_problem_by_key_value("frontendQuestionId", frontend_question_id)
        return problem.get("titleSlug", None)

    def problem_data_from_path(self, filepath: str) -> Tuple[str, str, str]:
        """
        Parses the problem data from the solution file path.

        Args:
            filepath (str): The solution file path.

        Returns:
            Tuple[str, str, str]: A tuple containing (question_id, title_slug, file_extension).

        Raises:
            ProblemSetError: If the filepath format is invalid.
        """
        filename = os.path.basename(filepath)
        parts = filename.split('.')
        if len(parts) != 3:
            logger.error("Invalid filepath format. Expected {question_id}.{title_slug}.{file_extension}.")
            raise ProblemSetError("Invalid filepath format. Expected {question_id}.{title_slug}.{file_extension}.")
        frontend_id, title_slug, file_extension = parts[0], parts[1], parts[2]
        return frontend_id, title_slug, file_extension
