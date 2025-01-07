import json
import os
import platform
import logging
import re
from typing import Dict

from leetcode_cli.exceptions.exceptions import ConfigError

logger = logging.getLogger(__name__)

class ConfigManager:
    """
    Manages loading and saving of configuration settings.
    """
    def __init__(self):
        self.config_path = self.get_config_path()
        self.config_dir = os.path.dirname(self.config_path)
        self.config = self.load_config()

    @staticmethod
    def get_config_path() -> str:
        """
        Determines the configuration file path based on the operating system.
        """
        if platform.system() == "Windows":
            config_dir = os.getenv("APPDATA", os.path.expanduser("~\\AppData\\Roaming"))
            return os.path.join(config_dir, "leetcode", "config.json")

        else: # macOS, Linux
            config_dir = os.path.expanduser("~/.config/leetcode")
            return os.path.join(config_dir, "config.json")

    def load_config(self) -> Dict:
        """
        Loads the configuration from the config file.
        """
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return json.load(f)

            except json.JSONDecodeError:
                logger.warning("config.json is corrupted. Returning empty config.")
                return {}

            except OSError as e:
                logger.error(f"Failed to read config file: {e}")
                raise ConfigError("Failed to read config file.")
        else:
            logger.info("config.json not found. Returning empty config.")
            return {}

    def save_config(self) -> None:
        """
        Saves the current configuration to the config file.
        """
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)

            logger.info(f"Configuration saved to {self.config_path}")

        except OSError as e:
            logger.error(f"Failed to save configuration: {e}")
            raise ConfigError("Failed to save configuration.")

    def set_key(self, key: str, value) -> None:
        """
        Sets a configuration key to a specified value.
        """
        self.config[key] = value
        self.save_config()

    def get_key(self, key: str, default=None):
        """
        Retrieves the value of a configuration key.
        """
        return self.config.get(key, default)

    def extract_csrf_token(self) -> str:
        """
        Extracts the CSRF token from the cookie string, if present.
        """
        cookie = self.get_key("cookie", "")
        match = re.search(r'csrftoken=([^;]+)', cookie)
        if match:
            return match.group(1)

        logger.error("CSRF token not found in the cookie.")
        return ""

    # Specific setters and getters for common keys
    def set_cookie(self, cookie: str) -> None:
        self.set_key("cookie", cookie)

    def get_cookie(self) -> str:
        return self.get_key("cookie", "")

    def set_username(self, username: str) -> None:
        self.set_key("username", username)

    def get_username(self) -> str:
        return self.get_key("username", "")

    def set_language(self, language: str) -> None:
        self.set_key("language", language)

    def get_language(self) -> str:
        return self.get_key("language", "")

    def set_chosen_problem(self, title_slug: str) -> None:
        self.set_key("chosen_problem", title_slug)

    def get_chosen_problem(self) -> str:
        return self.get_key("chosen_problem", "")
