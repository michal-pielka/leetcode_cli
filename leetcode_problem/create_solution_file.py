from ..data_fetching.fetch_code_snippet import fetch_code_snippet

def create_solution_file(title_slug, lang_slug):
    lang_slug_to_extension = {
        "cpp": "cpp",
        "java": "java",
        "python": "py",
        "python3": "py3",
        "c": "c",
        "csharp": "cs",
        "javascript": "js",
        "typescript": "ts",
        "php": "php",
        "swift": "swift",
        "kotlin": "kt",
        "dart": "dart",
        "golang": "go",
        "ruby": "rb",
        "scala": "scala",
        "rust": "rs",
        "racket": "rkt",
        "erlang": "erl",
        "elixir": "ex"
    }

    file_extension = lang_slug_to_extension[lang_slug]

    code_data = fetch_code_snippet(title_slug, lang_slug)
    code_snippet = code_data["code_snippet"]
    question_id = code_data["question_id"]
    title_slug = code_data["title_slug"]
    
    file_name = f"{question_id}.{title_slug}.{file_extension}"

    with open(file_name, 'w') as file:
        file.write(code_snippet)

