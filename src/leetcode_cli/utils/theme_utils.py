# theme_utils.py
import os
import json
import logging
from leetcode_cli.utils.config_utils import get_config_path, _load_config, _save_config
from leetcode_cli.constants.default_theme_constants import DEFAULT_THEME_FILES

logger = logging.getLogger(__name__)

def get_themes_dir():
    config_dir = os.path.dirname(get_config_path())
    return os.path.join(config_dir, "themes")

def list_themes():
    themes_dir = get_themes_dir()
    if not os.path.exists(themes_dir):
        return []
    return [d for d in os.listdir(themes_dir) if os.path.isdir(os.path.join(themes_dir, d))]

def set_current_theme(theme_name):
    if theme_name not in list_themes():
        logger.error(f"Theme '{theme_name}' does not exist.")
        return False
    config = _load_config()
    config["theme"] = theme_name
    _save_config(config)
    logger.info(f"Theme set to '{theme_name}'.")
    return True

def get_current_theme() -> str:
    """
    Retrieves the current theme name from the configuration.
    
    Returns:
        str: The name of the current theme. Defaults to 'default_theme' if not set.
    """
    config = _load_config()
    theme_name = config.get("theme", "default_theme")
    if not theme_name:
        print("theme not set")
        theme_name = "default_theme"
    return theme_name

def initialize_config_and_default_theme():
    config_path = get_config_path()
    config_dir = os.path.dirname(config_path)
    themes_dir = os.path.join(config_dir, "themes")
    default_theme_dir = os.path.join(themes_dir, "default_theme")

    # Create ~/.config/leetcode if it doesn't exist
    if not os.path.exists(config_dir):
        os.makedirs(config_dir, exist_ok=True)
        logger.info(f"Created configuration directory at '{config_dir}'.")

    # Create ~/.config/leetcode/themes if it doesn't exist
    if not os.path.exists(themes_dir):
        os.makedirs(themes_dir, exist_ok=True)
        logger.info(f"Created themes directory at '{themes_dir}'.")

    # If default_theme does not exist, create it from embedded data
    if not os.path.exists(default_theme_dir):
        os.makedirs(default_theme_dir, exist_ok=True)
        for filename, data in DEFAULT_THEME_FILES.items():
            file_path = os.path.join(default_theme_dir, filename)
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
        logger.info(f"Default theme created at '{default_theme_dir}'.")

def get_theme_data():
    """
    Loads and resolves the current theme data from the selected theme.
    
    Returns:
        dict: The resolved theme data with actual ANSI codes and symbols.
    """
    theme_name = get_current_theme()
    theme_path = os.path.join(get_themes_dir(), theme_name)
    default_path = os.path.join(get_themes_dir(), "default_theme")

    files_to_load = [
        "ansi_codes.json",
        "symbols.json",
        "interpretation_mappings.json",
        "problemset_mappings.json",
        "submission_mappings.json",
        "problem_mappings.json",
        "stats_mappings.json"
    ]

    theme_data = {
        "ANSI_CODES": {},
        "SYMBOLS": {},
        "INTERPRETATION_ANSI_CODES": {},
        "INTERPRETATION_SYMBOLS": {},
        "PROBLEMSET_FORMATTER_ANSI_CODES": {},
        "PROBLEMSET_FORMATTER_SYMBOLS": {},
        "SUBMISSION_ANSI_CODES": {},
        "SUBMISSION_SYMBOLS": {},
        "PROBLEM_FORMATTER_ANSI_CODES": {},
        "PROBLEM_FORMATTER_SYMBOLS": {},
        "STATS_FORMATTER_DIFFICULTY_COLORS": {},
        "STATS_FORMATTER_SYMBOLS": {}
    }

    def load_json(file_name):
        user_file = os.path.join(theme_path, file_name)
        default_file = os.path.join(default_path, file_name)
        if os.path.exists(user_file):
            path = user_file
        elif os.path.exists(default_file):
            path = default_file
        else:
            logger.warning(f"No '{file_name}' found in theme directories.")
            return {}
        try:
            with open(path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.error(f"Failed to parse '{file_name}'. Ensure it is valid JSON.")
            return {}

    # Load each file and merge keys
    for file in files_to_load:
        data = load_json(file)
        for key, val in data.items():
            theme_data[key] = val

    ansi_codes = theme_data["ANSI_CODES"]
    symbols = theme_data["SYMBOLS"]

    def resolve_ansi_refs(mapping_dict):
        for k, v in mapping_dict.items():
            if isinstance(v, str):
                # Split by space to handle stacked ANSI codes (e.g., "BABY_BLUE_BG WHITE BOLD")
                parts = v.split()
                combined_code = ""
                for part in parts:
                    code = ansi_codes.get(part)
                    if code:
                        combined_code += code
                    else:
                        logger.warning(f"ANSI code '{part}' not found in 'ANSI_CODES'.")
                mapping_dict[k] = combined_code

    def resolve_symbol_refs(mapping_dict):
        for k, v in mapping_dict.items():
            if isinstance(v, str):
                symbol_code = symbols.get(v)
                if symbol_code:
                    mapping_dict[k] = symbol_code
                else:
                    logger.warning(f"Symbol '{v}' not found in 'SYMBOLS'.")

    # Resolve references in all formatter mappings
    resolve_ansi_refs(theme_data["INTERPRETATION_ANSI_CODES"])
    resolve_symbol_refs(theme_data["INTERPRETATION_SYMBOLS"])

    resolve_ansi_refs(theme_data["PROBLEMSET_FORMATTER_ANSI_CODES"])
    resolve_symbol_refs(theme_data["PROBLEMSET_FORMATTER_SYMBOLS"])

    resolve_ansi_refs(theme_data["SUBMISSION_ANSI_CODES"])
    resolve_symbol_refs(theme_data["SUBMISSION_SYMBOLS"])

    resolve_ansi_refs(theme_data["PROBLEM_FORMATTER_ANSI_CODES"])
    resolve_symbol_refs(theme_data["PROBLEM_FORMATTER_SYMBOLS"])

    resolve_ansi_refs(theme_data["STATS_FORMATTER_DIFFICULTY_COLORS"])
    resolve_symbol_refs(theme_data["STATS_FORMATTER_SYMBOLS"])

    return theme_data
