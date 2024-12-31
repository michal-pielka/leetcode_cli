# leetcode_cli/core/init_app.py
import os
import json
import logging

from leetcode_cli.core.config_service import get_config_path, load_config, save_config, get_config_dir
from leetcode_cli.constants.default_config import DEFAULT_CONFIG_VALUES
from leetcode_cli.constants.themes.default_theme import DEFAULT_THEME_FILES
from leetcode_cli.constants.default_formatting_config import DEFAULT_FORMATTING_CONFIG
from leetcode_cli.core.theme_service import get_themes_dir

logger = logging.getLogger(__name__)


def initialize_leetcode_cli():
    """
    Called at CLI startup. Ensures:
      - ~/.config/leetcode folder exists
      - config.json exists & has required keys
      - formatting_config.json exists & has required keys
      - 'default_theme' folder & files exist
    """
    _ensure_config_directory()
    _ensure_minimum_config_fields()

    _ensure_formatting_config_file_exists()
    _ensure_minimum_formatting_config_fields_in_formatting()

    _ensure_default_theme_folder()


def _ensure_config_directory():
    config_path = get_config_path()
    config_dir = os.path.dirname(config_path)

    if not os.path.exists(config_dir):
        os.makedirs(config_dir, exist_ok=True)
        logger.info(f"Created configuration directory at '{config_dir}'.")


def _ensure_minimum_config_fields():
    """
    Make sure config.json has the keys from DEFAULT_CONFIG_VALUES.
    If missing/corrupted, recreate or fill defaults.
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
    If it's missing or corrupted (JSONDecodeError), recreate from default.
    """
    formatting_config_path = os.path.join(get_config_dir(), "formatting_config.json")

    if not os.path.exists(formatting_config_path):
        # File missing => create with defaults
        with open(formatting_config_path, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_FORMATTING_CONFIG, f, indent=4)
        logger.info(f"Created default formatting_config.json at '{formatting_config_path}'")
    else:
        # File present => try to load it
        try:
            with open(formatting_config_path, "r", encoding="utf-8") as f:
                json.load(f)  # Just to confirm we can read/parse it
        except (json.JSONDecodeError, OSError):
            # If it’s corrupt or unreadable => recreate from defaults
            logger.warning("formatting_config.json missing or corrupted. Recreating from defaults.")
            with open(formatting_config_path, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_FORMATTING_CONFIG, f, indent=4)
            logger.info(f"Recreated formatting_config.json with default content at '{formatting_config_path}'")


def _ensure_minimum_formatting_config_fields_in_formatting():
    """
    Loads the existing formatting_config.json (which we know exists),
    ensures top-level keys like 'interpretation', 'submission', 'problem_show' are present.
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
    Create themes/default_theme with the required JSON files if missing.
    We do not verify them thoroughly here, just ensure they're created if absent.
    """
    themes_dir = get_themes_dir()

    if not os.path.exists(themes_dir):
        os.makedirs(themes_dir, exist_ok=True)
        logger.info(f"Created themes directory at '{themes_dir}'")

    default_theme_dir = os.path.join(themes_dir, "default_theme")
    if not os.path.exists(default_theme_dir):
        os.makedirs(default_theme_dir, exist_ok=True)
        logger.info(f"Created default_theme directory at '{default_theme_dir}'")

        for filename, data in DEFAULT_THEME_FILES.items():
            file_path = os.path.join(default_theme_dir, filename)
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            logger.info(f"Created '{filename}' in default_theme.")
    else:
        logger.debug("default_theme folder already exists; not overwriting.")
