# leetcode_cli/utils/code_utils.py
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
