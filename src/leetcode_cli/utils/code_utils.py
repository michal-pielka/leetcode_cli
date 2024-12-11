# leetcode_cli/utils/code_utils.py
from leetcode_cli.utils.user_utils import get_language

def read_code_from_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def determine_language_from_extension(file_extension: str) -> str:
    extension_to_lang_slug = {
        "cpp": "cpp",
        "java": "java",
        "py": "python",
        "py3": "python3",
        "c": "c",
        "cs": "csharp",
        "js": "javascript",
        "ts": "typescript",
        "php": "php",
        "swift": "swift",
        "kt": "kotlin",
        "dart": "dart",
        "go": "golang",
        "rb": "ruby",
        "scala": "scala",
        "rs": "rust",
        "rkt": "racket",
        "erl": "erlang",
        "ex": "elixir"
    }
    lang = extension_to_lang_slug.get(file_extension.lower(), None)
    if not lang:
        raise ValueError(f"Unsupported file extension '{file_extension}'.")

    return lang


# These mappings could be moved here or imported from a central place
POSSIBLE_LANG_SLUGS = ["cpp", "java", "python", "python3", "c", "csharp", "javascript", "typescript", "php", "swift", "kotlin", "dart", "golang", "ruby", "scala", "rust", "racket", "erlang", "elixir"]
POSSIBLE_FILE_EXTENSIONS = ["cpp", "java", "py", "py3", "c", "cs", "js", "ts", "php", "swift", "kt", "dart", "go", "rb", "scala", "rs", "rkt", "erl", "ex"]

extension_to_lang_slug = {
    POSSIBLE_FILE_EXTENSIONS[i]: POSSIBLE_LANG_SLUGS[i] for i in range(len(POSSIBLE_LANG_SLUGS))
}

lang_slug_to_extension = {
    POSSIBLE_LANG_SLUGS[i]: POSSIBLE_FILE_EXTENSIONS[i] for i in range(len(POSSIBLE_FILE_EXTENSIONS))
}

def get_language_and_extension(file_extension=None):
    """
    Determine language and extension.

    If file_extension is provided, map it directly to language.
    If file_extension is None, use default language from config and map that to extension.
    """
    if file_extension:
        lang_slug = extension_to_lang_slug.get(file_extension.lower())
        if not lang_slug:
            return None, None

        return lang_slug, file_extension.lower()
    else:
        # Use default language from config
        lang_slug = get_language()
        if not lang_slug or lang_slug.lower() not in POSSIBLE_LANG_SLUGS:
            return None, None

        file_extension = lang_slug_to_extension.get(lang_slug.lower())
        if not file_extension:
            return None, None

        return lang_slug.lower(), file_extension.lower()

