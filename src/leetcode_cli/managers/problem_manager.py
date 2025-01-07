# problem_manager.py

import logging
from typing import Optional

from leetcode_cli.data_fetchers.problem_data_fetcher import (
    fetch_problem_id,
    fetch_problem_data,
    fetch_random_title_slug
)
from leetcode_cli.data_fetchers.interpretation_result_fetcher import fetch_interpretation_result
from leetcode_cli.data_fetchers.submission_result_fetcher import fetch_submission_result
from leetcode_cli.models.problem import Problem
from leetcode_cli.parsers.problem_data_parser import parse_problem_data
from leetcode_cli.exceptions.exceptions import FetchingError, ProblemError
from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.managers.problemset_manager import ProblemSetManager
logger = logging.getLogger(__name__)


class ProblemManager:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.problemset_manager = ProblemSetManager(config_manager)

    def get_problem_id(self, title_slug: str) -> int:
        try:
            data = fetch_problem_id(title_slug)
            question_id = data.get("data", {}).get("question", {}).get("questionId", None)
            if not question_id:
                raise FetchingError(f"Unable to find questionId for {title_slug}")

            return int(question_id)

        except FetchingError as fe:
            logger.error(fe)
            raise fe

    def get_problem_frontend_id(self, title_slug: str) -> int:
        try:
            data = fetch_problem_id(title_slug)
            question_id = data.get("data", {}).get("question", {}).get("questionFrontendId", None)
            if not question_id:
                raise FetchingError(f"Unable to find questionId for {title_slug}")

            return int(question_id)

        except FetchingError as fe:
            logger.error(fe)
            raise fe

    def get_title_slug_for_id(self, frontend_id: str) -> str:
        """
        Use ProblemSetManager to find the title slug from local metadata.
        """
        try:
            title_slug = self.problemset_manager.get_title_slug(frontend_id)
            if not title_slug:
                raise ProblemError(f"Title slug for frontend ID '{frontend_id}' not found in local metadata.")
            logger.debug(f"Title slug for frontend ID '{frontend_id}' is '{title_slug}'")
            return title_slug
        except Exception as e:
            logger.error(e)
            raise ProblemError(f"Error retrieving title slug for frontend ID '{frontend_id}': {e}")

    def get_specific_problem(self, identifier: str):
        """
        Return a `Problem` object (parsed) for either a slug or an ID.
        """
        try:
            if identifier.isdigit():
                # It's a numeric ID => frontend question ID
                title_slug = self.get_title_slug_for_id(identifier)
            else:
                # It's a slug
                title_slug = identifier

            raw_data = self.get_problem_data(title_slug)
            problem_obj = parse_problem_data(raw_data)
            logger.debug(f"Fetched Problem object for '{title_slug}'.")
            return problem_obj

        except ProblemError as pe:
            logger.error(pe)
            raise pe

    def get_random_problem(self, difficulty: Optional[str] = None, tags: Optional[list] = None) -> Problem:
        try:
            random_slug_data = fetch_random_title_slug(difficulty, tags)
            # the 'fetch_random_title_slug' returns a raw JSON with "data->randomQuestion->titleSlug"
            slug = random_slug_data.get("data", {}).get("randomQuestion", {}).get("titleSlug")
            if not slug:
                raise FetchingError("No random problem found with those filters.")

            raw_data = self.get_problem_data(slug)
            problem_obj = parse_problem_data(raw_data)
            
            # Store the slug in the problem object or return them separately
            # We will store it in problem_obj for convenience:
            problem_obj.__dict__["_title_slug"] = slug  # a hacky approach
            return problem_obj

        except FetchingError as fe:
            logger.error(fe)
            raise fe

    def get_problem_data(self, title_slug: str) -> dict:
        try:
            problem = fetch_problem_data(title_slug)
            return problem

        except FetchingError as fe:
            logger.error(fe)
            raise fe

    def run_code_interpretation(self, cookie, csrf_token, title_slug, code, language, testcases):
        try:
            qid = self.get_question_id_for_slug(title_slug)
            return fetch_interpretation_result(
                cookie, csrf_token, title_slug, code, language, testcases, qid
            )
        except FetchingError as fe:
            raise fe

    def submit_solution(self, cookie, csrf_token, title_slug, code, language):
        try:
            qid = self.get_question_id_for_slug(title_slug)
            return fetch_submission_result(
                cookie, csrf_token, title_slug, code, language, qid
            )
        except FetchingError as fe:
            raise fe
