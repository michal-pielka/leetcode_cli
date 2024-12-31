import json
import os
import platform
import logging
import re

from leetcode_cli.exceptions.exceptions import ConfigError

logger = logging.getLogger(__name__)

def get_config_path() -> str:
    """
    Determines the configuration file path (config.json)
    based on the operating system.
    """
    if platform.system() == "Windows":
        config_dir = os.getenv("APPDATA", os.path.expanduser("~\\AppData\\Roaming"))
        return os.path.join(config_dir, "leetcode", "config.json")
    else:  # macOS and Linux
        config_dir = os.path.expanduser("~/.config/leetcode")
        return os.path.join(config_dir, "config.json")

def get_config_dir() -> str:
    """Returns just the directory portion of the config path."""
    return os.path.dirname(get_config_path())

def load_config() -> dict:
    config_path = get_config_path()

    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                return json.load(f)

        except json.JSONDecodeError:
            logger.warning("Config file is corrupted. Starting with an empty config.")
    return {}

def save_config(config: dict):
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
    data = load_config()
    data["cookie"] = cookie
    save_config(data)

def set_username(username: str) -> None:
    data = load_config()
    data["username"] = username
    save_config(data)

def set_language(language: str) -> None:
    data = load_config()
    data["language"] = language
    save_config(data)

def set_chosen_problem(title_slug: str) -> None:
    data = load_config()
    data["chosen_problem"] = title_slug
    save_config(data)

def extract_csrf_token(cookie: str) -> str:
    try:
        match = re.search(r'csrftoken=([^;]+)', cookie)

    except Exception:
        return ""

    if match:
        return match.group(1)

    else:
        logger.error("CSRF token not found in the cookie.")
        return ""

def get_cookie() -> str:
    config = load_config()
    return config["cookie"]

def get_username() -> str:
    config = load_config()
    return config["username"]

def get_language() -> str:
    config = load_config()
    return config["language"]

def get_chosen_problem() -> str:
    config = load_config()
    return config["chosen_problem"]
