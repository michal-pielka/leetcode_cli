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

