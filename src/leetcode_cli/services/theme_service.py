import os
import logging
import yaml

from leetcode_cli.services.config_service import load_config, save_config, get_config_path
from leetcode_cli.exceptions.exceptions import ThemeError
from leetcode_cli.models.theme import ThemeData

logger = logging.getLogger(__name__)

def get_themes_dir() -> str:
    """
    Returns the path to ~/.config/leetcode/themes
    """
    config_dir = os.path.dirname(get_config_path())
    return os.path.join(config_dir, "themes")

def list_themes():
    """
    Returns the list of theme names (subdirectories) in the themes directory.
    """
    themes_dir = get_themes_dir()
    if not os.path.exists(themes_dir):
        return []
    return [d for d in os.listdir(themes_dir) if os.path.isdir(os.path.join(themes_dir, d))]

def get_current_theme() -> str:
    conf = load_config()
    return conf.get("theme", None)

def set_current_theme(theme_name: str) -> bool:
    """
    Sets 'theme' in config.json if the theme directory exists.
    """
    available = list_themes()
    if theme_name not in available:
        logger.error(f"Theme '{theme_name}' does not exist. Available: {available}")
        return False
    conf = load_config()
    conf["theme"] = theme_name
    save_config(conf)
    logger.info(f"Theme set to '{theme_name}'.")
    return True

def load_theme_data() -> ThemeData:
    """
    Reads the theme's YAML files (ansi_codes.yaml, symbols.yaml, mappings.yaml),
    merges them into a single ThemeData object.
    """
    theme = get_current_theme()
    if not theme:
        raise ThemeError("No theme is set in config.json. (key='theme')")

    ansi_data = _load_yaml_file(theme, "ansi_codes.yaml")
    if "ANSI_CODES" not in ansi_data:
        raise ThemeError(f"'ANSI_CODES' missing in ansi_codes.yaml for theme '{theme}'.")

    sym_data = _load_yaml_file(theme, "symbols.yaml")
    if "SYMBOLS" not in sym_data:
        raise ThemeError(f"'SYMBOLS' missing in symbols.yaml for theme '{theme}'.")

    mappings_data = _load_yaml_file(theme, "mappings.yaml")

    # Merge top-level
    merged = {
        "ANSI_CODES": ansi_data["ANSI_CODES"],
        "SYMBOLS": sym_data["SYMBOLS"],
        # Additional sub-dicts from mappings
        **mappings_data
    }

    return ThemeData(
        ANSI_CODES=merged["ANSI_CODES"],
        SYMBOLS=merged["SYMBOLS"],
        INTERPRETATION=merged.get("INTERPRETATION", {}),
        SUBMISSION=merged.get("SUBMISSION", {}),
        PROBLEMSET=merged.get("PROBLEMSET", {}),
        PROBLEM_DESCRIPTION=merged.get("PROBLEM_DESCRIPTION", {}),
        STATS_FORMATTER=merged.get("STATS_FORMATTER", {})
    )

def get_styling(theme_data: ThemeData, category: str, key: str) -> tuple:
    """
    Retrieves the ANSI code and symbols for a given category and key.

    :param theme_data: The ThemeData object.
    :param category: The category (e.g., 'INTERPRETATION', 'SUBMISSION').
    :param key: The specific key within the category.
    :return: A tuple of (ansi_code, symbol_left, symbol_right).
    """
    category_mapping = getattr(theme_data, category, {})
    if not category_mapping:
        raise ThemeError(f"ThemeData has no category '{category}' or it's empty.")
    if key not in category_mapping:
        raise ThemeError(f"Missing key '{key}' in theme category '{category}'.")

    mapping = category_mapping[key]
    ansi_chain = mapping.get("ansi", "")
    symbol_left = mapping.get("symbol_left", "")
    symbol_right = mapping.get("symbol_right", "")

    ansi_code = _resolve_ansi_chain(theme_data.ANSI_CODES, ansi_chain)
    symbol_left_resolved = _resolve_symbol_chain(theme_data.SYMBOLS, symbol_left)
    symbol_right_resolved = _resolve_symbol_chain(theme_data.SYMBOLS, symbol_right)

    return (ansi_code, symbol_left_resolved, symbol_right_resolved)

def _load_yaml_file(theme_name: str, filename: str) -> dict:
    """
    Loads a single YAML from the theme folder, returns its dict or raises ThemeError.
    """
    theme_dir = get_themes_dir()
    file_path = os.path.join(theme_dir, theme_name, filename)
    if not os.path.exists(file_path):
        raise ThemeError(f"File '{filename}' is missing for theme '{theme_name}'.")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            if not isinstance(data, dict):
                raise ThemeError(f"File '{filename}' is valid YAML but not a dictionary.")
            return data
    except yaml.YAMLError as e:
        raise ThemeError(f"File '{filename}' in theme '{theme_name}' is not valid YAML: {e}")

def _resolve_ansi_chain(ansi_codes_dict: dict, chain: str) -> str:
    """
    Resolves a comma-separated chain of ANSI code keys to a single ANSI code string.
    """
    if not chain:
        return ""
    tokens = [t.strip() for t in chain.split(',')]
    result = ""
    for token in tokens:
        if token.lower() not in ansi_codes_dict:
            raise ThemeError(f"Missing ANSI code '{token}' in 'ANSI_CODES'.")
        result += ansi_codes_dict[token.lower()]
    return result

def _resolve_symbol_chain(symbols_dict: dict, chain: str) -> str:
    """
    Resolves a comma-separated chain of symbol keys to a single symbol string.
    """
    if not chain:
        return ""
    tokens = [t.strip() for t in chain.split(',')]
    result = ""
    for token in tokens:
        if token.lower() not in symbols_dict:
            raise ThemeError(f"Missing symbol '{token}' in 'SYMBOLS'.")
        result += symbols_dict[token.lower()]
    return result
