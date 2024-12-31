# leetcode_cli/core/init_app.py
import os
import json
import logging

from leetcode_cli.core.config_service import get_config_path, load_config, save_config, get_config_dir
from leetcode_cli.constants.default_config import DEFAULT_CONFIG_VALUES
from leetcode_cli.constants.default_formatting_config import DEFAULT_FORMATTING_CONFIG
from leetcode_cli.core.theme_service import get_themes_dir
from leetcode_cli.constants.themes.default_theme.ansi_codes_yaml import ANSI_CODES_YAML
from leetcode_cli.constants.themes.default_theme.symbols_yaml import SYMBOLS_YAML
from leetcode_cli.constants.themes.default_theme.mappings_yaml import MAPPINGS_YAML

logger = logging.getLogger(__name__)

def initialize_leetcode_cli():
    """
    Called at CLI startup. Ensures:
      - ~/.config/leetcode folder exists
      - config.json exists & has required keys
      - formatting_config.json exists & has required keys
      - 'default_theme' folder & the three .yaml files exist
    """
    _ensure_config_directory()
    _ensure_minimum_config_fields()

    _ensure_formatting_config_file_exists()
    _ensure_minimum_formatting_config_fields_in_formatting()

    _ensure_default_theme_folder()

def _ensure_config_directory():
    """
    Ensures ~/.config/leetcode directory exists (based on platform).
    """
    config_path = get_config_path()
    config_dir = os.path.dirname(config_path)

    if not os.path.exists(config_dir):
        os.makedirs(config_dir, exist_ok=True)
        logger.info(f"Created configuration directory at '{config_dir}'.")

def _ensure_minimum_config_fields():
    """
    Make sure config.json has the keys from DEFAULT_CONFIG_VALUES.
    If missing/corrupted, fill defaults.
    """
    config = load_config()
    updated = False

    for key, default_value in DEFAULT_CONFIG_VALUES.items():
        if key not in config:
            config[key] = default_value
            logger.warning(f"Config missing '{key}', setting default: {default_value}")
            updated = True

    if updated:
        save_config(config)
        logger.info("Updated config.json with missing default fields.")

def _ensure_formatting_config_file_exists():
    """
    Ensures that formatting_config.json exists.
    If missing or corrupt, recreate from DEFAULT_FORMATTING_CONFIG.
    """
    formatting_config_path = os.path.join(get_config_dir(), "formatting_config.json")

    if not os.path.exists(formatting_config_path):
        # File missing => create with defaults
        with open(formatting_config_path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_FORMATTING_CONFIG, f, indent=4)
        logger.info(f"Created default formatting_config.json at '{formatting_config_path}'")
    else:
        # File present => check if valid
        try:
            with open(formatting_config_path, "r", encoding="utf-8") as f:
                json.load(f)  # Just confirm it can parse
        except (json.JSONDecodeError, OSError):
            logger.warning("formatting_config.json missing or corrupted. Recreating from defaults.")
            with open(formatting_config_path, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_FORMATTING_CONFIG, f, indent=4)
            logger.info(f"Recreated formatting_config.json with default content at '{formatting_config_path}'")

def _ensure_minimum_formatting_config_fields_in_formatting():
    """
    Loads the existing formatting_config.json and ensures top-level keys
    ('interpretation', 'submission', 'problem_show') are present.
    If missing, fill from defaults and save.
    """
    formatting_config_path = os.path.join(get_config_dir(), "formatting_config.json")

    with open(formatting_config_path, "r", encoding="utf-8") as f:
        user_data = json.load(f)

    updated = False
    for key, default_val in DEFAULT_FORMATTING_CONFIG.items():
        if key not in user_data:
            user_data[key] = default_val
            logger.warning(f"formatting_config.json missing '{key}', using defaults.")
            updated = True

    if updated:
        with open(formatting_config_path, "w", encoding="utf-8") as f:
            json.dump(user_data, f, indent=4)
        logger.info("Updated formatting_config.json with missing top-level sections.")

def _ensure_default_theme_folder():
    """
    Ensures that the folder ~/.config/leetcode/themes/default_theme/ exists
    and that the three YAML files (ansi_codes.yaml, symbols.yaml, mappings.yaml)
    are written if not present.
    """
    themes_dir = get_themes_dir()
    default_theme_dir = os.path.join(themes_dir, "default_theme")

    os.makedirs(default_theme_dir, exist_ok=True)

    # Now create the three files if they don't exist:
    _write_if_missing(default_theme_dir, "ansi_codes.yaml", ANSI_CODES_YAML)
    _write_if_missing(default_theme_dir, "symbols.yaml", SYMBOLS_YAML)
    _write_if_missing(default_theme_dir, "mappings.yaml", MAPPINGS_YAML)

def _write_if_missing(theme_dir: str, filename: str, content: str):
    file_path = os.path.join(theme_dir, filename)
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        logger.info(f"Created '{filename}' in '{theme_dir}'")
    else:
        logger.debug(f"'{filename}' already exists; not overwriting.")
