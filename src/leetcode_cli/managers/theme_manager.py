import os
import logging
import yaml
from typing import List, Optional

from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.exceptions.exceptions import ThemeError
from leetcode_cli.models.theme import ThemeData

logger = logging.getLogger(__name__)

class ThemeManager:
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.themes_dir = self.get_themes_dir()
        self.theme_data = None

    def get_themes_dir(self) -> str:
        config_dir = os.path.dirname(self.config_manager.config_path)
        return os.path.join(config_dir, "themes")

    def list_themes(self) -> List[str]:
        if not os.path.exists(self.themes_dir):
            logger.warning(f"Themes directory '{self.themes_dir}' does not exist.")
            return []
        themes = [
            d for d in os.listdir(self.themes_dir)
            if os.path.isdir(os.path.join(self.themes_dir, d))
        ]
        logger.debug(f"Available themes: {themes}")
        return themes

    def get_current_theme(self) -> Optional[str]:
        return self.config_manager.get_key("theme", None)

    def set_current_theme(self, theme_name: str) -> bool:
        available_themes = self.list_themes()
        if theme_name not in available_themes:
            logger.error(f"Theme '{theme_name}' does not exist. Available themes: {available_themes}")
            return False
        self.config_manager.set_key("theme", theme_name)
        logger.info(f"Theme set to '{theme_name}'.")
        return True

    def load_theme_data(self) -> ThemeData:
        theme_name = self.get_current_theme()
        if not theme_name:
            raise ThemeError("No theme is set in config.json. (key='theme')")

        ansi_data = self._load_yaml_file(theme_name, "ansi_codes.yaml")
        symbols_data = self._load_yaml_file(theme_name, "symbols.yaml")
        mappings_data = self._load_yaml_file(theme_name, "mappings.yaml")

        if "ANSI_CODES" not in ansi_data:
            raise ThemeError(f"'ANSI_CODES' missing in ansi_codes.yaml for theme '{theme_name}'.")
        if "SYMBOLS" not in symbols_data:
            raise ThemeError(f"'SYMBOLS' missing in symbols.yaml for theme '{theme_name}'.")

        merged = {
            "ANSI_CODES": ansi_data["ANSI_CODES"],
            "SYMBOLS": symbols_data["SYMBOLS"],
            **mappings_data
        }
        logger.debug(f"Theme data for '{theme_name}': {merged}")

        return ThemeData(
            ANSI_CODES=merged["ANSI_CODES"],
            SYMBOLS=merged["SYMBOLS"],
            INTERPRETATION=merged.get("INTERPRETATION", {}),
            SUBMISSION=merged.get("SUBMISSION", {}),
            PROBLEMSET=merged.get("PROBLEMSET", {}),
            PROBLEM_DESCRIPTION=merged.get("PROBLEM_DESCRIPTION", {}),
            STATS_FORMATTER=merged.get("STATS_FORMATTER", {})
        )

    def get_styling(self, section: str, key: str) -> tuple:
        """
        Returns (combined_ansi_code, combined_symbol_left, combined_symbol_right).
        E.g., ("\033[32m\033[1m", "✔ ", "")
        """
        if not self.theme_data:
            self.theme_data = self.load_theme_data()

        # Grab the dictionary from e.g. self.theme_data.INTERPRETATION["Accepted"]
        try:
            section_data = getattr(self.theme_data, section)
            raw_mapping = section_data[key]
        except AttributeError:
            raise ThemeError(f"Section '{section}' not found in theme data.")
        except KeyError:
            raise ThemeError(f"Key '{key}' not found in section '{section}'.")

        # raw_mapping might look like:
        #   { "ansi": "green,bold", "symbol_left": "checkmark,space", "symbol_right": "" }

        # Parse the 'ansi' field to produce combined ANSI codes:
        combined_ansi = self._parse_ansi_codes(raw_mapping.get("ansi", ""))

        # Parse the symbol_left/symbol_right fields to produce combined strings:
        combined_left = self._parse_symbols(raw_mapping.get("symbol_left", ""))
        combined_right = self._parse_symbols(raw_mapping.get("symbol_right", ""))

        return (combined_ansi, combined_left, combined_right)

    def _parse_ansi_codes(self, ansi_field: str) -> str:
        """
        Convert something like "green,bold" -> actual ANSI code from self.theme_data.ANSI_CODES
        e.g. "\u001b[38;2;80;250;123m" + "\u001b[1m".
        """
        if not ansi_field:
            return ""
        codes = ansi_field.split(',')
        final = ""
        for code_key in codes:
            code_key = code_key.strip().lower()
            # e.g. code_key = "green" or "bold"
            ansi_code_dict = self.theme_data.ANSI_CODES
            # Attempt to get e.g. ansi_code_dict["green"] or ansi_code_dict["bold"]
            if code_key in ansi_code_dict:
                final += ansi_code_dict[code_key]
            else:
                # If we can't find it in ANSI_CODES, ignore or log?
                logger.warning(f"ANSI code '{code_key}' not found in theme ANSI_CODES. Skipping.")
        return final

    def _parse_symbols(self, symbol_field: str) -> str:
        """
        Convert "checkmark,space" -> "✔ ".
        Looks up each from self.theme_data.SYMBOLS or returns them literally if not found.
        """
        if not symbol_field:
            return ""
        parts = symbol_field.split(',')
        final = ""
        for p in parts:
            p = p.strip().lower()
            # e.g. "checkmark", "space", "dot"
            if p in self.theme_data.SYMBOLS:
                final += self.theme_data.SYMBOLS[p]
            else:
                # If not found, we can just add it literally.
                final += p
        return final

    def _load_yaml_file(self, theme_name: str, filename: str) -> dict:
        file_path = os.path.join(self.themes_dir, theme_name, filename)
        if not os.path.exists(file_path):
            raise ThemeError(f"File '{filename}' is missing for theme '{theme_name}'.")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if not isinstance(data, dict):
                    raise ThemeError(f"File '{filename}' for theme '{theme_name}' is not a valid dictionary.")
                return data
        except yaml.YAMLError as e:
            raise ThemeError(f"YAML error in '{filename}' for theme '{theme_name}': {e}")
