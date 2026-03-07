import logging
import os

import yaml

from leetcode_cli.exceptions.exceptions import ThemeError
from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.models.theme import ThemeData

logger = logging.getLogger(__name__)


class ThemeManager:
    """
    Manages theme loading and retrieval of specific styling for each section/key.

    Public methods:
      - list_themes()
      - get_current_theme()
      - set_current_theme()
      - load_theme_data()
      - get_styling()

    Private helpers:
      - _get_themes_dir()
      - _parse_ansi_codes()
      - _parse_symbols()
      - _load_yaml_file()
    """

    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.themes_dir = self.get_themes_dir()  # moved the helper call to a private function
        self.theme_data: ThemeData | None = None

    #
    # ──────────────────────────────────────────────────────
    #   PUBLIC METHODS
    # ──────────────────────────────────────────────────────
    #

    def get_themes_dir(self) -> str:
        """
        Private helper to locate the "~/.leetcode/themes" directory.
        """
        config_dir = os.path.dirname(self.config_manager.config_path)
        return os.path.join(config_dir, "themes")

    def list_themes(self) -> list[str]:
        """
        Returns a list of available theme directories.
        """
        if not os.path.exists(self.themes_dir):
            logger.warning(f"Themes directory '{self.themes_dir}' does not exist.")
            return []

        themes = [d for d in os.listdir(self.themes_dir) if os.path.isdir(os.path.join(self.themes_dir, d))]

        logger.debug(f"Available themes: {themes}")
        return themes

    def get_current_theme(self) -> str | None:
        """
        Returns the currently set theme from config.json.
        """
        return self.config_manager.get_theme()

    def set_current_theme(self, theme_name: str) -> bool:
        """
        Sets the current theme to 'theme_name', if it exists in the list of installed themes.
        """
        available_themes = self.list_themes()
        if theme_name not in available_themes:
            logger.error(f"Theme '{theme_name}' does not exist. Available themes: {available_themes}")
            return False

        self.config_manager.set_theme(theme_name)
        logger.info(f"Theme set to '{theme_name}'.")

        return True

    def load_theme_data(self) -> ThemeData:
        """
        Loads the theme data from local YAML files into a ThemeData object.
        Raises ThemeError if mandatory fields or files are missing.
        """
        theme_name = self.get_current_theme()
        if not theme_name:
            raise ThemeError("No theme is set in config.json. (key='theme')")

        ansi_data = self._load_yaml_file(theme_name, "ansi_codes.yaml")
        symbols_data = self._load_yaml_file(theme_name, "symbols.yaml")
        styles_data = self._load_yaml_file(theme_name, "styles.yaml")

        if "ANSI_CODES" not in ansi_data:
            raise ThemeError(f"'ANSI_CODES' missing in ansi_codes.yaml for theme '{theme_name}'.")

        if "SYMBOLS" not in symbols_data:
            raise ThemeError(f"'SYMBOLS' missing in symbols.yaml for theme '{theme_name}'.")

        logger.debug(f"Theme data loaded for '{theme_name}'.")

        self.theme_data = ThemeData(
            ANSI_CODES=ansi_data["ANSI_CODES"],
            SYMBOLS=symbols_data["SYMBOLS"],
            styles=styles_data,
        )
        return self.theme_data

    def get_styling(self, section: str, key: str) -> tuple:
        """
        Returns (combined_ansi_code, icon_string).
        E.g., ("\033[32m\033[1m", "✔")
        """
        if not self.theme_data:
            self.theme_data = self.load_theme_data()

        section_data = self.theme_data.styles.get(section)
        if section_data is None:
            raise ThemeError(f"Section '{section}' not found in theme styles.")

        raw_mapping = section_data.get(key)
        if raw_mapping is None:
            raise ThemeError(f"Key '{key}' not found in section '{section}'.")

        combined_ansi = self._parse_ansi_codes(raw_mapping.get("style", ""))
        icon = self._parse_symbols(raw_mapping.get("icon", ""))

        return (combined_ansi, icon)

    def get_layout_value(self, key: str, default=None):
        """
        Returns a value from the 'layout' section of the theme styles.
        """
        if not self.theme_data:
            self.theme_data = self.load_theme_data()

        layout = self.theme_data.styles.get("layout", {})
        return layout.get(key, default)

    #
    # ──────────────────────────────────────────────────────
    #   PRIVATE METHODS
    # ──────────────────────────────────────────────────────
    #

    def _parse_ansi_codes(self, ansi_field: str) -> str:
        """
        Convert "green,bold" -> combined ANSI codes from self.theme_data.ANSI_CODES.
        Raises ThemeError if a code isn't found in 'ANSI_CODES'.
        """
        if not ansi_field:
            return ""

        codes = ansi_field.split(",")
        final = ""
        for code_key in codes:
            code_key = code_key.strip().lower()
            if code_key not in self.theme_data.ANSI_CODES:
                raise ThemeError(
                    f"ANSI code '{code_key}' not found in 'ANSI_CODES' mapping. Theme configuration is malformed."
                )
            final += self.theme_data.ANSI_CODES[code_key]

        return final

    def _parse_symbols(self, symbol_field: str) -> str:
        """
        Convert "checkmark,space" -> "✔ ".
        Raises ThemeError if symbol isn't found in 'SYMBOLS'.
        """
        if not symbol_field:
            return ""

        parts = symbol_field.split(",")
        final = ""
        for p in parts:
            p = p.strip().lower()
            if p not in self.theme_data.SYMBOLS:
                raise ThemeError(f"Symbol '{p}' not found in 'SYMBOLS' mapping. Theme configuration is malformed.")
            final += self.theme_data.SYMBOLS[p]
        return final

    def _load_yaml_file(self, theme_name: str, filename: str) -> dict:
        """
        Private helper to load a YAML file from the theme's folder.
        Raises ThemeError if file is missing or invalid.
        """
        file_path = os.path.join(self.themes_dir, theme_name, filename)
        if not os.path.exists(file_path):
            raise ThemeError(f"File '{filename}' is missing for theme '{theme_name}'.")

        try:
            with open(file_path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if not isinstance(data, dict):
                    raise ThemeError(f"File '{filename}' for theme '{theme_name}' is not a valid dictionary.")
                return data

        except yaml.YAMLError as e:
            raise ThemeError(f"YAML error in '{filename}' for theme '{theme_name}': {e}") from e
