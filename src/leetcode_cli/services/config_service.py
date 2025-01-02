import json
import os
import platform
import logging
import re

logger = logging.getLogger(__name__)

def get_config_path() -> str:
    """
    Determines where config.json lives based on OS.
    """
    if platform.system() == "Windows":
        config_dir = os.getenv("APPDATA", os.path.expanduser("~\\AppData\\Roaming"))
        return os.path.join(config_dir, "leetcode", "config.json")
    else:  # macOS, Linux
        config_dir = os.path.expanduser("~/.config/leetcode")
        return os.path.join(config_dir, "config.json")

def get_config_dir() -> str:
    return os.path.dirname(get_config_path())

def load_config() -> dict:
    config_path = get_config_path()
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                return json.load(f)

        except json.JSONDecodeError:
            logger.warning("config.json is corrupted. Returning empty config.")
            return {}

    return {}

def save_config(config: dict):
    """
    Save config to ~/.config/leetcode/config.json.
    Assumes directory/file already created by init_app_files.py.
    """
    config_path = get_config_path()
    try:
        with open(config_path, "w") as f:
            json.dump(config, f, indent=4)
        logger.info(f"Configuration saved to {config_path}")
    except OSError as e:
        logger.error(f"Failed to save configuration: {e}")

def set_cookie(cookie: str):
    data = load_config()
    data["cookie"] = cookie
    save_config(data)

def set_username(username: str):
    data = load_config()
    data["username"] = username
    save_config(data)

def set_language(language: str):
    data = load_config()
    data["language"] = language
    save_config(data)

def set_chosen_problem(title_slug: str):
    data = load_config()
    data["chosen_problem"] = title_slug
    save_config(data)

def extract_csrf_token(cookie: str) -> str:
    """
    Extracts the CSRF token from the cookie string (if present).
    """
    try:
        match = re.search(r'csrftoken=([^;]+)', cookie)
        if match:
            return match.group(1)
    except Exception:
        pass

    logger.error("CSRF token not found in the cookie.")
    return ""

def get_cookie() -> str:
    return load_config().get("cookie", "")

def get_username() -> str:
    return load_config().get("username", "")

def get_language() -> str:
    return load_config().get("language", "")

def get_chosen_problem() -> str:
    return load_config().get("chosen_problem", "")
