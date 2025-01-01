import os
import logging
import yaml

from leetcode_cli.services.config_service import get_config_path, load_config, save_config, get_config_dir
from leetcode_cli.constants.default_config import DEFAULT_CONFIG_VALUES
from leetcode_cli.constants.default_formatting_config import DEFAULT_FORMATTING_CONFIG_YAML
from leetcode_cli.constants.themes.default_theme.symbols_yaml import SYMBOLS_YAML
from leetcode_cli.constants.themes.default_theme.ansi_codes_yaml import ANSI_CODES_YAML
from leetcode_cli.constants.themes.default_theme.mappings_yaml import MAPPINGS_YAML
from leetcode_cli.services.theme_service import get_themes_dir

logger = logging.getLogger(__name__)

def initialize_leetcode_cli():
    _ensure_config_directory()
    _ensure_minimum_config_fields()

    _ensure_formatting_config_file_exists()
    _ensure_minimum_formatting_config_fields()

    _ensure_default_theme_folder()

def _ensure_config_directory():
    config_path = get_config_path()
    config_dir = os.path.dirname(config_path)

    if not os.path.exists(config_dir):
        os.makedirs(config_dir, exist_ok=True)
        logger.info(f"Created configuration directory at '{config_dir}'.")

def _ensure_minimum_config_fields():
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
    Ensures ~/.config/leetcode/formatting_config.yaml exists,
    creating it from DEFAULT_FORMATTING_CONFIG_YAML if missing or corrupt.
    """
    formatting_config_path = os.path.join(get_config_dir(), "formatting_config.yaml")

    if not os.path.exists(formatting_config_path):
        # File missing => create with defaults
        with open(formatting_config_path, "w", encoding="utf-8") as f:
            f.write(DEFAULT_FORMATTING_CONFIG_YAML)
        logger.info(f"Created default formatting_config.yaml at '{formatting_config_path}'")
    else:
        # Check if valid YAML
        try:
            with open(formatting_config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if not data or not isinstance(data, dict):
                    raise ValueError("Not a dict or empty")
        except (yaml.YAMLError, ValueError):
            logger.warning("formatting_config.yaml missing or corrupted. Recreating from defaults.")
            with open(formatting_config_path, "w", encoding="utf-8") as f:
                f.write(DEFAULT_FORMATTING_CONFIG_YAML)
            logger.info(f"Recreated formatting_config.yaml with default content at '{formatting_config_path}'")

def _ensure_minimum_formatting_config_fields():
    """
    Ensures 'interpretation', 'submission', 'problem_show' exist in formatting_config.yaml
    If any missing, merges from DEFAULT_FORMATTING_CONFIG_YAML.
    """
    from yaml import safe_load, dump

    formatting_config_path = os.path.join(get_config_dir(), "formatting_config.yaml")

    with open(formatting_config_path, "r", encoding="utf-8") as f:
        user_data = safe_load(f)

    # Convert our default YAML -> dict
    default_data = safe_load(DEFAULT_FORMATTING_CONFIG_YAML)

    updated = False
    for key, default_val in default_data.items():
        if key not in user_data:
            user_data[key] = default_val
            logger.warning(f"formatting_config.yaml missing '{key}', adding defaults.")
            updated = True

    if updated:
        with open(formatting_config_path, "w", encoding="utf-8") as f:
            f.write(dump(user_data, sort_keys=False))
        logger.info("Updated formatting_config.yaml with missing top-level sections.")

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
