import os
import logging
import json
import yaml
from typing import List, Dict, Any

# NEW references
from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.managers.theme_manager import ThemeManager
from leetcode_cli.constants.default_config import DEFAULT_CONFIG_VALUES
from leetcode_cli.constants.default_formatting_config import DEFAULT_FORMATTING_CONFIG_YAML

logger = logging.getLogger(__name__)

def initialize_leetcode_cli():
    """
    Main entry point to ensure all necessary files and folders exist in ~/.config/leetcode/.
    This function is idempotent—safe to call multiple times without harm.
    """
    try:
        # Instantiate the config_manager
        config_manager = ConfigManager()
        # Grab the paths
        config_dir = config_manager.config_dir
        config_path = config_manager.config_path

        _ensure_config_directory(config_dir)
        _ensure_config_file_exists(config_path)
        _ensure_minimum_config_fields(config_manager)

        _ensure_formatting_config_file_exists(config_dir)
        _ensure_minimum_formatting_config_fields(config_dir)

        # Use the theme manager to get the themes_dir
        theme_manager = ThemeManager(config_manager)
        themes_dir = theme_manager.get_themes_dir()
        _ensure_themes_directory(themes_dir)

        available_themes = _discover_available_themes()
        for theme_name in available_themes:
            _ensure_theme_folder(theme_name, theme_manager)

    except Exception as e:
        logger.error(f"Failed to initialize LeetCode CLI: {e}", exc_info=True)
        raise

def _ensure_config_directory(config_dir: str):
    """
    Creates ~/.config/leetcode directory if it does not exist.
    """
    try:
        os.makedirs(config_dir, exist_ok=True)
        logger.info(f"Ensured configuration directory exists at '{config_dir}'.")

    except Exception as e:
        logger.error(f"Error creating configuration directory '{config_dir}': {e}")
        raise


def _ensure_config_file_exists(config_path: str):
    """
    Creates ~/.config/leetcode/config.json file if it does not exist.
    """
    if not os.path.exists(config_path):
        try:
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=4)

            logger.info(f"Created empty config.json at '{config_path}'.")

        except Exception as e:
            logger.error(f"Error creating config.json at '{config_path}': {e}")
            raise

    else:
        logger.debug(f"config.json at '{config_path}' already exists.")

def _ensure_minimum_config_fields(config_manager: ConfigManager):
    config = config_manager.config
    updated = False

    for key, default_value in DEFAULT_CONFIG_VALUES.items():
        if key not in config:
            config[key] = default_value
            logger.warning(f"Config missing '{key}', setting default: {default_value}")
            updated = True

    if updated:
        config_manager.save_config()
        logger.info("Updated config.json with missing default fields.")

    else:
        logger.debug("No missing fields in config.json; no updates needed.")

def _ensure_formatting_config_file_exists(config_dir:str):
    """
    Creates ~/.config/leetcode/formatting_config.yaml if it does not exist,
    or re-creates it if the existing file is corrupted/unusable.
    """
    formatting_path = os.path.join(config_dir, "formatting_config.yaml")

    if not os.path.exists(formatting_path):
        try:
            with open(formatting_path, "w", encoding="utf-8") as f:
                f.write(DEFAULT_FORMATTING_CONFIG_YAML)

            logger.info(f"Created default formatting_config.yaml at '{formatting_path}'.")

        except Exception as e:
            logger.error(f"Error creating formatting_config.yaml at '{formatting_path}': {e}")
            raise e

        return

    # If it already exists, verify it's valid YAML
    try:
        with open(formatting_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if not isinstance(data, dict):
                raise ValueError("formatting_config.yaml is not a valid dictionary.")

        logger.debug("formatting_config.yaml is valid.")

    except (yaml.YAMLError, ValueError) as e:
        logger.warning(f"formatting_config.yaml is corrupted or invalid: {e}. Recreating from defaults.")

        try:
            with open(formatting_path, "w", encoding="utf-8") as f:
                f.write(DEFAULT_FORMATTING_CONFIG_YAML)

            logger.info(f"Recreated formatting_config.yaml at '{formatting_path}'.")

        except Exception as ex:
            logger.error(f"Error recreating formatting_config.yaml at '{formatting_path}': {ex}")
            raise


def _ensure_minimum_formatting_config_fields(config_dir: str):
    """
    Fills ~/.config/leetcode/formatting_config.yaml with top-level sections
    if they’re missing (e.g., 'interpretation', 'submission', 'problem_show').
    """
    formatting_path = os.path.join(config_dir, "formatting_config.yaml")

    try:
        with open(formatting_path, "r", encoding="utf-8") as f:
            user_data = yaml.safe_load(f) or {}

        default_data = yaml.safe_load(DEFAULT_FORMATTING_CONFIG_YAML)
        updated = False

        for key, default_section in default_data.items():
            if key not in user_data:
                user_data[key] = default_section
                logger.warning(f"formatting_config.yaml missing '{key}', adding defaults.")
                updated = True

        if updated:
            with open(formatting_path, "w", encoding="utf-8") as f:
                yaml.dump(user_data, f, sort_keys=False)
            logger.info("Updated formatting_config.yaml with missing sections.")
        else:
            logger.debug("No missing sections in formatting_config.yaml; no updates needed.")

    except Exception as e:
        logger.error(f"Error ensuring minimum formatting config fields: {e}")
        raise e


def _ensure_themes_directory(themes_dir: str):
    """
    Creates ~/.config/leetcode/themes directory if it doesn't exist.
    """
    try:
        os.makedirs(themes_dir, exist_ok=True)
        logger.info(f"Ensured themes directory exists at '{themes_dir}'.")

    except Exception as e:
        logger.error(f"Error creating themes directory '{themes_dir}': {e}")
        raise


def _discover_available_themes() -> List[str]:
    """
    Discovers available themes by listing subdirectories in the constants/themes directory.
    Returns a list of theme names.
    """
    themes_constants_dir = os.path.join(os.path.dirname(__file__), 'constants', 'themes')
    try:
        themes = [
            name for name in os.listdir(themes_constants_dir)
            if os.path.isdir(os.path.join(themes_constants_dir, name)) and not name.startswith("__")
        ]

        logger.info(f"Discovered themes: {themes}")

        return themes

    except Exception as e:
        logger.error(f"Error discovering available themes in '{themes_constants_dir}': {e}")
        raise

def _ensure_theme_folder(theme_name: str, theme_manager: ThemeManager):
    """
    Ensures that a theme folder exists in ~/.config/leetcode/themes/{theme_name},
    and that it contains the necessary YAML files (ansi_codes.yaml, symbols.yaml, mappings.yaml).
    """
    themes_dir = theme_manager.get_themes_dir()
    theme_constants_dir = os.path.join(os.path.dirname(__file__), 'constants', 'themes', theme_name)
    theme_user_dir = os.path.join(themes_dir, theme_name)

    try:
        os.makedirs(theme_user_dir, exist_ok=True)
        logger.info(f"Ensured theme directory exists at '{theme_user_dir}'.")

    except Exception as e:
        logger.error(f"Error creating theme directory '{theme_user_dir}': {e}")
        raise

    yaml_files = {
        "ansi_codes.yaml": "ANSI_CODES_YAML",
        "symbols.yaml": "SYMBOLS_YAML",
        "mappings.yaml": "MAPPINGS_YAML"
    }

    for filename, var_name in yaml_files.items():
        _write_yaml_if_missing(theme_constants_dir, theme_user_dir, filename, var_name)

def _write_yaml_if_missing(source_dir: str, target_dir: str, filename: str, variable_name: str):
    """
    Helper to create the theme YAML file if it doesn't exist already by extracting
    the YAML content from the corresponding Python module variable.
    """
    source_file = os.path.join(source_dir, f"{filename.replace('.yaml', '')}_yaml.py")
    target_file = os.path.join(target_dir, filename)

    if not os.path.exists(target_file):
        try:
            yaml_content = _extract_yaml_from_py(source_file, variable_name)
            if yaml_content:
                with open(target_file, "w", encoding="utf-8") as f:
                    f.write(yaml_content)
                logger.info(f"Created '{filename}' in '{target_dir}'.")

            else:
                logger.error(f"YAML content for '{variable_name}' not found in '{source_file}'.")

        except Exception as e:
            logger.error(f"Error writing '{filename}' in '{target_dir}': {e}")
            raise

    else:
        logger.debug(f"'{filename}' already exists in '{target_dir}'; not overwriting.")


def _extract_yaml_from_py(file_path: str, variable_name: str) -> str:
    """
    Safely extracts the YAML string from a Python file by executing it in a controlled namespace.
    Returns the YAML string if found, else an empty string.
    """
    namespace: Dict[str, Any] = {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            exec(f.read(), namespace)

        yaml_content = namespace.get(variable_name, "")

        if not isinstance(yaml_content, str):
            logger.error(f"Variable '{variable_name}' in '{file_path}' is not a string.")
            return ""

        return yaml_content

    except Exception as e:
        logger.error(f"Error extracting '{variable_name}' from '{file_path}': {e}")
        
        return ""

if __name__ == "__main__":
    initialize_leetcode_cli()
