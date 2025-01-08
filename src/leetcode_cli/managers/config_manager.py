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
        self.config_path = self._get_config_path()
        self.config_dir = os.path.dirname(self.config_path)
        self.config = self._load_config()

    #
    # ──────────────────────────────────────────────────────
    #   PUBLIC METHODS
    # ──────────────────────────────────────────────────────
    #

    def _set_key(self, key: str, value) -> None:
        """
        Sets a configuration key to a specified value.
        """
        self.config[key] = value
        self.save_config()

    def _get_key(self, key: str, default=None):
        """
        Retrieves the value of a configuration key.
        """
        return self.config.get(key, default)

    def set_cookie(self, cookie: str) -> None:
        self._set_key("cookie", cookie)

    def get_cookie(self) -> str:
        return self._get_key("cookie", "")

    def set_username(self, username: str) -> None:
        self._set_key("username", username)

    def get_username(self) -> str:
        return self._get_key("username", "")

    def set_language(self, language: str) -> None:
        self._set_key("language", language)

    def get_language(self) -> str:
        return self._get_key("language", "")

    def set_chosen_problem(self, title_slug: str) -> None:
        self._set_key("chosen_problem", title_slug)

    def get_chosen_problem(self) -> str:
        return self._get_key("chosen_problem", "")

    def set_theme(self, theme_name: str):
        self._set_key("theme", theme_name)

    def get_theme(self) -> str:
        return self._get_key("theme", "")

    def get_csrf_token(self) -> str:
        """
        Extracts the CSRF token from the cookie string, if present.
        """
        cookie = self._get_key("cookie", "")
        match = re.search(r"csrftoken=([^;]+)", cookie)
        if match:
            return match.group(1)

        logger.error("CSRF token not found in the cookie.")
        return ""

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

    #
    # ──────────────────────────────────────────────────────
    #   PRIVATE HELPERS
    # ──────────────────────────────────────────────────────
    #

    @staticmethod
    def _get_config_path() -> str:
        """
        Determines the configuration file path based on the operating system.
        """
        if platform.system() == "Windows":
            # Use APPDATA for application data directory on Windows, fallback to Roaming
            config_dir = os.getenv("APPDATA", os.path.expanduser("~\\AppData\\Roaming"))
            config_dir = os.path.join(config_dir, "leetcode")

        else:
            # Use ~/.leetcode for Unix-like systems
            config_dir = os.path.expanduser("~/.leetcode")

        # Ensure the directory exists before returning the full path
        os.makedirs(config_dir, exist_ok=True)
        return os.path.join(config_dir, "config.json")

    def _load_config(self) -> Dict:
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
