import os

from leetcode_cli.services.config_service import get_language
from leetcode_cli.constants.problem_constants import LANG_SLUG_TO_EXTENSION, EXTENSION_TO_LANG_SLUG, POSSIBLE_LANG_SLUGS

def read_code_from_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def determine_language_from_extension(file_extension: str) -> str:
    lang = EXTENSION_TO_LANG_SLUG.get(file_extension.lower(), None)
    if not lang:
        raise ValueError(f"Unsupported file extension '{file_extension}'.")

    return lang

def get_language_and_extension(file_extension=None):
    """
    Determine language and extension.

    If file_extension is provided, map it directly to language.
    If file_extension is None, use default language from config and map that to extension.
    """
    if file_extension:
        lang_slug = EXTENSION_TO_LANG_SLUG.get(file_extension.lower())
        if not lang_slug:
            return None, None

        return lang_slug, file_extension.lower()
    else:
        # Use default language from config
        lang_slug = get_language()
        if not lang_slug or lang_slug.lower() not in POSSIBLE_LANG_SLUGS:
            return None, None

        file_extension = LANG_SLUG_TO_EXTENSION.get(lang_slug.lower())
        if not file_extension:
            return None, None

        return lang_slug.lower(), file_extension.lower()

def create_solution_file(question_id: str, title_slug: str, file_extension: str, code_snippet: str) -> None:
    """
    Creates a solution file with the provided code snippet.

    code_snippet is expected to be a dictionary containing at least a 'code' key with the snippet string.
    If code_snippet is None or doesn't have code, fall back to a default template.
    """

    file_name = f"{question_id}.{title_slug}.{file_extension}"

    if os.path.exists(file_name):
        logger.warning(f"File '{file_name}' already exists. Not overwriting.")
        return

    try:
        with open(file_name, 'w', encoding='utf-8') as f:
            f.write(code_snippet)
        logger.info(f"Solution file '{file_name}' created successfully.")
    except OSError as e:
        logger.error(f"Failed to create solution file '{file_name}': {e}")
        raise
