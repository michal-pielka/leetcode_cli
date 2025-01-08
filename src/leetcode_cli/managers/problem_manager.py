# file: managers/problem_manager.py

import logging
from typing import Optional, Tuple, List

from leetcode_cli.managers.auth_service import AuthService
from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.managers.problemset_manager import ProblemSetManager

from leetcode_cli.exceptions.exceptions import FetchingError, ProblemError
from leetcode_cli.models.problem import Problem

# Import fetchers + parsers needed
from leetcode_cli.data_fetchers.problem_data_fetcher import (
    fetch_problem_data, fetch_random_title_slug, fetch_problem_testcases, fetch_problem_id, fetch_problem_frontend_id
)
from leetcode_cli.data_fetchers.interpretation_result_fetcher import fetch_interpretation_result
from leetcode_cli.data_fetchers.submission_result_fetcher import fetch_submission_result

from leetcode_cli.parsers.problem_data_parser import parse_problem_data
from leetcode_cli.parsers.interpretation_result_parser import parse_interpretation_result
from leetcode_cli.parsers.submission_result_parser import parse_submission_result

logger = logging.getLogger(__name__)


class ProblemManager:
    """
    Manages fetching & parsing problem-related data from LeetCode,
    using AuthService for authentication. The commands call these
    manager methods, then pass the results to a formatter for display.

    Enhancements:
      - Before network fetch, attempt to load data from problemset metadata.
      - If metadata is empty or no matching data found, fallback to network.
    """

    def __init__(self, config_manager: ConfigManager, auth_service: AuthService, problemset_manager: ProblemSetManager):
        self.config_manager = config_manager
        self.auth_service = auth_service
        self.problemset_manager = problemset_manager

    #
    # ──────────────────────────────────────────────────────
    #   PUBLIC METHODS
    # ──────────────────────────────────────────────────────
    #

    def get_specific_problem(self, identifier: str) -> Problem:
        """
        Return a parsed `Problem` object for either an ID or a slug.
        1) If it's an ID, tries local metadata => fallback fetch if not found
        2) If it's a slug, tries direct fetch
        """
        # If numeric => interpret as front-end ID
        if identifier.isdigit():
            title_slug = self.get_title_slug_for_frontend_id(identifier)

        else:
            title_slug = identifier

        raw_data = fetch_problem_data(title_slug)
        problem_obj = parse_problem_data(raw_data)
        logger.debug(f"Parsed problem data for slug '{title_slug}'.")

        return problem_obj

    def get_random_problem(self, difficulty: Optional[str] = None, tags: Optional[List[str]] = None) -> Problem:
        """
        Fetch a random problem slug, parse the resulting problem,
        and return a Problem object.

        1) Try picking a random local problem that matches difficulty/tags.
        2) If no local match or metadata empty, fallback to network.
        """
        title_slug = self.problemset_manager.get_random_local_problem_slug(difficulty, tags)

        if not title_slug:
            slug_from_net = fetch_random_title_slug(difficulty=difficulty, tags=tags)
            title_slug = slug_from_net.get("data", {}).get("randomQuestion", {}).get("titleSlug", "")

        if not title_slug:
            raise FetchingError("No random problem found with those filters.")

        raw_data = fetch_problem_data(title_slug)
        problem_obj = parse_problem_data(raw_data)
        problem_obj.__dict__["_title_slug"] = title_slug

        return problem_obj

    def get_problem_frontend_id(self, title_slug: str) -> int:
        """
        Return numeric front-end question ID for the given slug.
        1) Attempt local metadata => fallback to network.
        """
        # Try local metadata first
        local_frontend_id = self._try_local_frontend_id_by_slug(title_slug)

        if local_frontend_id:
            return int(local_frontend_id)

        raw = fetch_problem_frontend_id(title_slug)
        frontend_id = raw.get("data", {}).get("question", {}).get("questionFrontendId")

        if not frontend_id:
            raise FetchingError(f"Unable to find frontend question ID for slug: '{title_slug}'")

        return int(frontend_id)

    def get_problem_id(self, title_slug: str) -> int:
        """
        Return the internal questionId for a given slug.
        Attempt local => fallback network.
        """
        # Try local metadata frist
        local_id = self._try_local_id_by_slug(title_slug)

        if local_id:
            return int(local_id)

        raw = fetch_problem_id(title_slug)
        question_id = raw.get("data", {}).get("question", {}).get("questionId")

        if not question_id:
            raise FetchingError(f"Unable to find questionId for slug: '{title_slug}'")

        return int(question_id)

    def get_title_slug_for_frontend_id(self, frontend_id: str) -> str:
        """
        Use local metadata to find the slug from the ID. Raises ProblemError if not found,
        fallback => attempt a network approach if you prefer (like listing all problems).
        """
        title_slug = self._try_local_slug_by_frontend_id(frontend_id)

        if title_slug:
            logger.debug(f"Title slug for ID '{frontend_id}' is '{title_slug}' (from local).")
            return title_slug

        raise ProblemError(f"Title slug for frontend ID '{frontend_id}' not found in local metadata.")

    def get_interpretation_result(
        self, title_slug: str, code: str, lang_slug: str, testcases: str
    ):
        """
        Return a fully parsed InterpretationResult for 'Run Code' action.
        """
        raw = fetch_interpretation_result(
            cookie=self.auth_service.get_cookie(),
            csrf_token=self.auth_service.get_csrf_token(),
            title_slug=title_slug,
            code=code,
            language=lang_slug,
            testcases=testcases,
            question_id=self.get_problem_id(title_slug)
        )
        return parse_interpretation_result(raw)

    def get_submission_result(
        self, title_slug: str, code: str, lang_slug: str
    ):
        """
        Return a fully parsed SubmissionResult for the final 'submit' action.
        """
        raw = fetch_submission_result(
            cookie=self.auth_service.get_cookie(),
            csrf_token=self.auth_service.get_csrf_token(),
            title_slug=title_slug,
            code=code,
            language=lang_slug,
            question_id=self.get_problem_id(title_slug),
        )
        return parse_submission_result(raw)

    def get_example_testcases(self, title_slug: str) -> str:
        """
        Manager method for fetching example testcases from the problem detail.
        """
        try:
            data = fetch_problem_testcases(title_slug)
            return data.get('data', {}).get('question', {}).get('exampleTestcases', "")

        except FetchingError as fe:
            logger.error(f"Could not fetch example testcases: {fe}")
            raise fe

    def problem_data_from_path(self, filepath: str) -> Tuple[str, str, str]:
        """
        Parses the problem data from the solution file path.

        Raises ProblemError if format is invalid.
        """
        import os
        filename = os.path.basename(filepath)
        parts = filename.split('.')

        if len(parts) != 3:
            logger.error("Invalid filepath format. Expected {question_id}.{title_slug}.{file_extension}.")
            raise ProblemError("Invalid filepath format. Expected {question_id}.{title_slug}.{file_extension}.")

        return parts[0], parts[1], parts[2]

    #
    # ──────────────────────────────────────────────────────
    #   PRIVATE HELPERS
    # ──────────────────────────────────────────────────────
    #

    def _try_local_frontend_id_by_slug(self, title_slug: str) -> str:
        """
        Attempt to find front-end ID by searching local metadata.
        If not found, return None.
        """
        problem = self.problemset_manager.get_problem_by_key_value(key="titleSlug", value=title_slug)

        if not problem:
            return ""

        return problem.get("frontendQuestionId", "")

    def _try_local_id_by_slug(self, title_slug: str) -> str:
        """
        Attempt to find front-end ID by searching local metadata.
        If not found, return None.
        """
        problem = self.problemset_manager.get_problem_by_key_value(key="titleSlug", value=title_slug)

        if not problem:
            return ""

        return problem.get("questionId", "")
    
    def _try_local_slug_by_frontend_id(self, frontend_id: str) -> str:
        """
        Attempt to find front-end ID by searching local metadata.
        If not found, return None.
        """
        problem = self.problemset_manager.get_problem_by_key_value(key="frontendQuestionId", value=frontend_id)

        if not problem:
            return ""

        return problem.get("titleSlug", "")
