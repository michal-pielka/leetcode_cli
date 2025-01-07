import os
import logging
from typing import Optional, Tuple

from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.constants.problem_constants import LANG_SLUG_TO_EXTENSION, EXTENSION_TO_LANG_SLUG, POSSIBLE_LANG_SLUGS
from leetcode_cli.exceptions.exceptions import CodeError

from leetcode_cli.data_fetchers.code_snippet_fetcher import fetch_code_snippet

logger = logging.getLogger(__name__)


class CodeManager:
    """
    Manages code-related functionalities, including reading and creating solution files.
    """
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager

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
            with open(file_path, 'r', encoding='utf-8') as f:
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

    def get_language_and_extension(self, file_extension: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
        """
        Determines the programming language and its file extension.

        Args:
            file_extension (Optional[str]): The file extension provided by the user.

        Returns:
            Tuple[Optional[str], Optional[str]]: The language slug and its file extension.
        """
        if file_extension:
            lang_slug = EXTENSION_TO_LANG_SLUG.get(file_extension.lower())
            if not lang_slug:
                logger.error(f"Unsupported file extension '{file_extension}'.")
                return None, None

            logger.debug(f"Language '{lang_slug}' determined from extension '{file_extension}'.")

            return lang_slug, file_extension.lower()

        else:
            lang_slug = self.config_manager.get_language()
            if not lang_slug or lang_slug.lower() not in POSSIBLE_LANG_SLUGS:
                logger.error("Invalid or undefined language in configuration.")
                return None, None

            ext = LANG_SLUG_TO_EXTENSION.get(lang_slug.lower())
            if not ext:
                logger.error(f"File extension for language '{lang_slug}' not found.")
                return None, None

            logger.debug(f"Language '{lang_slug}' with extension '{ext}' determined from configuration.")

            return lang_slug.lower(), ext.lower()

    def create_solution_file(self, question_id: str, title_slug: str, file_extension: str, code_snippet: str) -> None:
        """
        Creates a new solution file with the provided code snippet.

        Args:
            question_id (str): The numeric ID of the problem.
            title_slug (str): The title slug of the problem.
            file_extension (str): The file extension based on the programming language.
            code_snippet (str): The code to be written into the solution file.

        Raises:
            CodeError: If the file cannot be created.
        """
        file_name = f"{question_id}.{title_slug}.{file_extension}"

        if os.path.exists(file_name):
            logger.warning(f"Solution file '{file_name}' already exists. Not overwriting.")
            raise CodeError(f"Solution file '{file_name}' already exists.")

        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(code_snippet)

            logger.info(f"Solution file '{file_name}' created successfully.")

        except OSError as e:
            logger.error(f"Failed to create solution file '{file_name}': {e}")
            raise CodeError(f"Failed to create solution file '{file_name}': {e}")

    def create_solution_file_with_snippet(self, question_id: str, title_slug: str, lang_slug: str, file_extension: str) -> None:
        """
        Fetches the code snippet and creates the solution file.

        Args:
            question_id (str): The numeric ID of the problem.
            title_slug (str): The title slug of the problem.
            lang_slug (str): The language slug.
            file_extension (str): The file extension.

        Raises:
            CodeError: If fetching the code snippet or creating the file fails.
        """
        try:
            code_data = fetch_code_snippet(title_slug, lang_slug)
            snippet_list = code_data.get('data', {}).get('question', {}).get('codeSnippets', [])
            code_str = ""
            for sn in snippet_list:
                if sn.get('langSlug') == lang_slug:
                    code_str = sn.get('code', "")
                    break

            if not code_str:
                code_str = f"# Solution for {title_slug} in {lang_slug}\n\n"

            self.create_solution_file(question_id, title_slug, file_extension, code_str)
            file_name = f"{question_id}.{title_slug}.{file_extension}"
            logger.debug(f"Solution file '{file_name}' has been created successfully.")

        except Exception as e:
            logger.error(f"Failed to create solution file with snippet: {e}")
            raise CodeError(f"Failed to create solution file with snippet: {e}")
