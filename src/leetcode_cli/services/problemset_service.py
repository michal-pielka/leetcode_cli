import logging
import os
import json

from leetcode_cli.services.config_service import get_config_path

logger = logging.getLogger(__name__)

def get_problems_data_path() -> str:
    """
    Typically ~/.config/leetcode/problems_metadata.json
    """
    config_dir = os.path.dirname(get_config_path())
    return os.path.join(config_dir, "problems_metadata.json")

def load_problemset_metadata() -> dict:
    """
    Loads the local JSON file that caches problemset data.
    """
    path = get_problems_data_path()
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.warning("problems_metadata.json is corrupted. Returning empty.")
    return {}

def save_problemset_metadata(data: dict) -> None:
    """
    Overwrites the problems_metadata.json with 'data'.
    """
    path = get_problems_data_path()
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        logger.info(f"Problemset data saved to {path}")
    except OSError as e:
        logger.error(f"Failed to save problemset data: {e}")

def get_problem_by_key_value(problems_data, key, value):
    questions = problems_data.get('data', {}).get('problemsetQuestionList', {}).get('questions', [])
    for problem in questions:
        if str(problem.get(key, "")).lower() == str(value).lower():
            return problem
    logger.warning(f"Problem with {key}='{value}' not found in cached data.")
    return {}

def filter_problems(problems_data, difficulty=None, tags=None):
    """
    Filters the given problems_data by difficulty, tags, etc.
    """
    questions = problems_data.get('data', {}).get('problemsetQuestionList', {}).get('questions', [])
    if not questions:
        logger.error("No questions in problemset data.")
        return None

    # Filter by difficulty
    if difficulty:
        difficulty_cap = difficulty.capitalize()
        questions = [q for q in questions if q.get('difficulty', '').capitalize() == difficulty_cap]
        if not questions:
            logger.warning(f"No problems found with difficulty '{difficulty}'.")
            return None

    # Filter by tags
    if tags:
        tags_lower = {t.lower() for t in tags}
        filtered = []
        for q in questions:
            problem_tags = q.get('topicTags', [])
            slugs = {tag['slug'].lower() for tag in problem_tags}
            if tags_lower.issubset(slugs):
                filtered.append(q)
        questions = filtered
        if not questions:
            logger.warning(f"No problems found with tags: {tags}.")
            return None

    return questions

def select_random_problem(questions):
    if not questions:
        return None
    from random import choice
    selected = choice(questions)
    logger.info(f"Random problem selected: {selected.get('title', 'Unknown')} (Slug: {selected.get('titleSlug')})")
    return selected

def problem_data_from_path(filepath):
    """
    Example: '1.two-sum.py' => (question_id='1', title_slug='two-sum', file_ext='py')
    """
    filename = os.path.basename(filepath)
    parts = filename.split('.')
    if len(parts) != 3:
        raise ValueError("Invalid filepath format. Expected {question_id}.{title_slug}.{file_extension}")
    frontend_id = parts[0]
    title_slug = parts[1]
    file_extension = parts[2]
    return frontend_id, title_slug, file_extension
