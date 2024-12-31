from leetcode_cli.core.config_service import get_language
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

