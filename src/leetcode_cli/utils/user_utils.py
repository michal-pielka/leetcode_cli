import json
import os
import platform
import logging

logger = logging.getLogger(__name__)

def get_config_path() -> str:
    """
    Determines the configuration file path based on the operating system.

    Returns:
        str: The full path to the configuration file.
    """
    if platform.system() == "Windows":
        config_dir = os.getenv("APPDATA", os.path.expanduser("~\\AppData\\Roaming"))
        config_path = os.path.join(config_dir, "leetcode", "config.json")
    else:  # macOS and Linux
        config_dir = os.path.expanduser("~/.config/leetcode")
        config_path = os.path.join(config_dir, "config.json")
    return config_path

def get_problems_data_path() -> str:
    """
    Determines the path to the problems data file.

    Returns:
        str: The full path to the problems data file.
    """
    config_dir = os.path.dirname(get_config_path())
    problems_path = os.path.join(config_dir, "problems_metadata.json")
    return problems_path

def _load_config():
    """
    Loads the configuration from the config file.

    Returns:
        dict: The configuration dictionary.
    """
    config_path = get_config_path()
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.warning("Config file is corrupted. Starting with an empty config.")
    return {}


def load_problems_metadata() -> dict:
    """
    Loads the cached problems metadata from the local JSON file.

    Returns:
        dict: The loaded problems metadata. Returns an empty dictionary if the file doesn't exist or is corrupted.
    """
    problems_path = get_problems_data_path()
    if os.path.exists(problems_path):
        try:
            with open(problems_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.warning("Problems data file is corrupted. Starting with an empty problems data.")
    return {}

def _save_config(config):
    """
    Saves the configuration dictionary to the config file.

    Args:
        config (dict): The configuration dictionary to save.
    """
    config_path = get_config_path()
    config_dir = os.path.dirname(config_path)
    try:
        os.makedirs(config_dir, exist_ok=True)
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)
        logger.info(f"Configuration saved to {config_path}")
    except OSError as e:
        logger.error(f"Failed to save configuration: {e}")

def set_cookie(cookie: str) -> None:
    """
    Sets the user's cookie in the configuration file.

    Args:
        cookie (str): The cookie string to save.
    """
    config = _load_config()
    config["cookie"] = cookie
    _save_config(config)

def set_username(username: str) -> None:
    """
    Sets the user's username in the configuration file.

    Args:
        username (str): The username to save.
    """
    config = _load_config()
    config["username"] = username
    _save_config(config)

def set_language(language: str) -> None:
    """
    Sets the user's preferred programming language in the configuration file.

    Args:
        language (str): The programming language to save.
    """
    config = _load_config()
    config["language"] = language
    _save_config(config)

def set_chosen_problem(title_slug: str) -> None:
    """
    Sets the solution file path in the configuration file.

    Args:
        file_path (str): The solution file path to save.
    """
    config = _load_config()
    config["chosen_problem"] = title_slug
    _save_config(config)

def extract_csrf_token(cookie: str) -> str:
    """
    Extracts the CSRF token from the cookie string.

    Args:
        cookie (str): The cookie string.

    Returns:
        str: The CSRF token if found, else an empty string.
    """
    import re
    try:
        match = re.search(r'csrftoken=([^;]+)', cookie)

    except Exception:
        return None

    if match:
        return match.group(1)
    else:
        logger.error("CSRF token not found in the cookie.")
        return None

def get_cookie():
    config = _load_config()
    cookie = config.get("cookie", None)

    if not cookie:
        logger.error("Cookie not found in configuration.")

    return cookie

def get_username():
    config = _load_config()
    username = config.get("username", None)

    if not username:
        logger.error("Username not found in configuration.")
        
    return username

def get_language():
    config = _load_config()
    language = config.get("language", None)

    if not language:
        logger.error("Language not found in configuration.")

    return language

def get_chosen_problem():
    config = _load_config()
    chosen_problem = config.get("chosen_problem", None)

    if not chosen_problem:
        logger.error("Solution file path not found in configuration.")

    return chosen_problem

# New functions for handling problems data

def save_problems_data(data: dict) -> None:
    """
    Saves the problems metadata to a local JSON file.

    Args:
        data (dict): The problems metadata to save.
    """
    problems_path = get_problems_data_path()
    try:
        os.makedirs(os.path.dirname(problems_path), exist_ok=True)
        with open(problems_path, "w") as f:
            json.dump(data, f, indent=4)
        logger.info(f"Problems data saved to {problems_path}")
    except OSError as e:
        logger.error(f"Failed to save problems data: {e}")



def get_problem_by_key_value(problems_data, key, value):
    questions = problems_data.get('data', {}).get('problemsetQuestionList', {}).get('questions', [])

    for problem in questions:
        if str(problem.get(key, "")).lower() == str(value).lower():
            return problem

    logger.warning(f"Problem with {key}='{value}' not found in cached data.")

    return {}

def filter_problems(problems_data, difficulty=None, tags=None):
    """
    Filters the given problems data based on difficulty and tags.

    Args:
        problems_data (dict): The problems metadata.
        difficulty (str, optional): The difficulty level ('Easy', 'Medium', 'Hard'). Defaults to None.
        tags (list of str, optional): A list of tag slugs to filter by. Defaults to None.

    Returns:
        list: The list of filtered problems.
    """
    # Extract the list of questions
    questions = problems_data.get('data', {}).get('problemsetQuestionList', {}).get('questions', [])
    
    if not questions:
        logger.error("No questions found in problems data.")
        return None

    # Apply difficulty filter if specified
    if difficulty:
        difficulty_capitalize = difficulty.capitalize()

        questions = [q for q in questions if q.get('difficulty', '').capitalize() == difficulty_capitalize]
        if not questions:
            logger.warning(f"No problems found with difficulty '{difficulty}'.")
            return None

    # Apply tags filter if specified
    if tags:
        tags_lower = set(tag.lower() for tag in tags)
        filtered_questions = []
        for q in questions:
            problem_tags = q.get('topicTags', [])
            if not problem_tags:
                continue 

            problem_tags_slugs = set(tag['slug'].lower() for tag in problem_tags)
            if tags_lower.issubset(problem_tags_slugs):
                filtered_questions.append(q)

        questions = filtered_questions
        if not questions:
            logger.warning(f"No problems found with tags {', '.join(tags)}.")
            return None

    return questions

def select_random_problem(questions):
    """
    Selects a random problem from the given list of questions.

    Args:
        questions (list): List of problem metadata dictionaries.

    Returns:
        dict: The randomly selected problem's data, or None if the list is empty.
    """
    if not questions:
        return None

    import random

    selected_problem = random.choice(questions)
    logger.info(f"Random problem selected: {selected_problem.get('title', 'Unknown Title')} (Slug: {selected_problem.get('titleSlug', 'N/A')})")
    return selected_problem

def problem_data_from_path(filepath):
    filename = os.path.basename(filepath)
    # Split the filename by the dots to extract parts
    parts = filename.split('.')
    if len(parts) != 3:
        raise ValueError("Invalid filepath format. Expected {question_id}.{title_slug}.{file_extension}")
    
    # Extract parts
    frontend_id = parts[0]
    title_slug = '.'.join(parts[1:-1])  # Join middle parts as the title_slug can have dots
    file_extension = parts[-1]
    
    return frontend_id, title_slug, file_extension
