import os
import logging

logger = logging.getLogger(__name__)

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
