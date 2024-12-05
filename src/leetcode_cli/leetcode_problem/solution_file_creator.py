import logging
from leetcode_cli.data_fetching.code_snippet_fetcher import fetch_code_snippet

logger = logging.getLogger(__name__)

def create_solution_file(question_id, title_slug, lang_slug, file_extension):
    """
    Creates a solution file with the code snippet for the specified problem and language.

    Args:
        title_slug (str): The title slug of the problem.
        lang_slug (str): The language slug.

    Raises:
        Exception: If fetching data or file creation fails.
    """
    if not question_id:
        raise ValueError("Question id cant be None")

    if not title_slug:
        raise ValueError("Title slug cant be None")

    if not lang_slug:
        raise ValueError(f"Unsupported language slug: '{lang_slug}'")

    if not file_extension:
        raise ValueError(f"Unsupported file extension: '{file_extension}'")


    # Fetch code snippet
    code_snippet = fetch_code_snippet(title_slug, lang_slug)

    file_name = f"{question_id}.{title_slug}.{file_extension}"

    try:
        with open(file_name, 'w') as file:
            file.write(code_snippet)

    except IOError as e:
        raise Exception(f"Failed to create solution file '{file_name}': {e}")

    logger.info(f"Solution file '{file_name}' created successfully.")
