import os
import logging

from typing import Tuple

from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.constants.problem_constants import (
    EXTENSION_TO_LANG_SLUG,
    LANG_SLUG_TO_EXTENSION,
)
from leetcode_cli.exceptions.exceptions import CodeError
from leetcode_cli.data_fetchers.code_snippet_fetcher import fetch_code_snippet

logger = logging.getLogger(__name__)


class CodeManager:
    """
    Manages code-related functionalities, including reading and creating solution files.
    Handles:
      - Reading local code files
      - Inferring language & extension
      - Fetching code snippets and creating solution files
    """

    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager

    #
    # ──────────────────────────────────────────────────────
    #   PUBLIC METHODS
    # ──────────────────────────────────────────────────────
    #

    def read_code_from_file(self, file_path: str) -> str:
        """
        Reads and returns the content of a code file.

        Args:
            file_path (str): The path to the code file.

        Returns:
            str: The content of the code file.

        Raises:
            CodeError: If the file cannot be read.
        """
        if not os.path.exists(file_path):
            logger.error(f"File '{file_path}' does not exist.")
            raise CodeError(f"File '{file_path}' does not exist.")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
                logger.debug(f"Read code from file '{file_path}'.")
                return code

        except OSError as e:
            logger.error(f"Failed to read file '{file_path}': {e}")
            raise CodeError(f"Failed to read file '{file_path}': {e}")

    def determine_language_from_extension(self, file_extension: str) -> str:
        """
        Determines the programming language based on the file extension.

        Args:
            file_extension (str): The file extension (e.g., 'py', 'cpp').

        Returns:
            str: The corresponding language slug.

        Raises:
            CodeError: If the file extension is unsupported.
        """
        lang = EXTENSION_TO_LANG_SLUG.get(file_extension.lower())
        if not lang:
            logger.error(f"Unsupported file extension '{file_extension}'.")
            raise CodeError(f"Unsupported file extension '{file_extension}'.")

        logger.debug(f"Determined language '{lang}' from extension '{file_extension}'.")
        return lang

    def get_default_lang_and_ext(self) -> Tuple[str, str]:
        """
        Attempts to retrieve the default language from the user's config,
        then derive the matching extension from LANG_SLUG_TO_EXTENSION.

        Returns:
            (lang_slug, file_extension)

        Raises:
            CodeError: If config language is undefined or unsupported.
        """
        config_lang = self.config_manager.get_language()  # e.g. "python"
        if not config_lang:
            raise CodeError("No default language is set in config.")

        extension = LANG_SLUG_TO_EXTENSION.get(config_lang.lower())
        if not extension:
            raise CodeError(f"No known extension for default language '{config_lang}'.")

        logger.debug(f"Default language '{config_lang}' => extension '{extension}'.")
        return config_lang.lower(), extension.lower()

    def infer_lang_and_ext(self, user_ext: str = "") -> Tuple[str, str]:
        """
        Infers the (lang_slug, file_extension) from either:
        1) user-provided extension (e.g. ".cpp" or "py"), or
        2) config default if user_ext is empty.

        Returns:
            (lang_slug, file_extension)

        Raises:
            CodeError: If either approach fails.
        """
        # If user provided an extension (like ".cpp" or "cpp")
        if user_ext:
            # Remove leading '.' if any
            file_extension = user_ext.lstrip(".").lower()
            lang_slug = self.determine_language_from_extension(file_extension)
            return lang_slug, file_extension

        # Else, fallback to the default from config
        return self.get_default_lang_and_ext()

    def create_solution_file_with_snippet(
        self, frontend_id: str, title_slug: str, lang_slug: str, file_extension: str
    ) -> None:
        """
        Fetches the code snippet and creates the solution file.

        Args:
            frontend_id (str): The numeric ID of the problem.
            title_slug (str): The title slug of the problem.
            lang_slug (str): The language slug.
            file_extension (str): The file extension.

        Raises:
            CodeError: If fetching the code snippet or creating the file fails.
        """
        try:
            code_data = fetch_code_snippet(title_slug, lang_slug)
            snippet_list = (
                code_data.get("data", {}).get("question", {}).get("codeSnippets", [])
            )
            code_str = ""
            for sn in snippet_list:
                if sn.get("langSlug") == lang_slug:
                    code_str = sn.get("code", "")
                    break

            if not code_str:
                code_str = f"# That problem does not have a code snippet for {lang_slug} and is probably not submittable in that language.\n\n"

            self._create_solution_file(
                frontend_id, title_slug, file_extension, code_str
            )
            file_name = f"{frontend_id}.{title_slug}.{file_extension}"
            logger.debug(f"Solution file '{file_name}' has been created successfully.")

        except Exception as e:
            logger.error(f"Failed to create solution file with snippet: {e}")
            raise CodeError(f"Failed to create solution file with snippet: {e}")

    #
    # ──────────────────────────────────────────────────────
    #   PRIVATE HELPERS
    # ──────────────────────────────────────────────────────
    #

    def _create_solution_file(
        self, frontend_id: str, title_slug: str, file_extension: str, code_snippet: str
    ) -> None:
        """
        Creates a new solution file with the provided code snippet.

        Args:
            frontend_id (str): The numeric ID of the problem (a/k/a frontendId).
            title_slug (str): The title slug of the problem.
            file_extension (str): e.g. "py", "cpp", etc.
            code_snippet (str): The code to be written into the solution file.

        Raises:
            CodeError: If the file cannot be created (e.g. file already exists).
        """
        file_name = f"{frontend_id}.{title_slug}.{file_extension}"

        if os.path.exists(file_name):
            logger.warning(
                f"Solution file '{file_name}' already exists. Not overwriting."
            )
            raise CodeError(f"Solution file '{file_name}' already exists.")

        try:
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(code_snippet)

            logger.info(f"Solution file '{file_name}' created successfully.")

        except OSError as e:
            logger.error(f"Failed to create solution file '{file_name}': {e}")
            raise CodeError(f"Failed to create solution file '{file_name}': {e}")
