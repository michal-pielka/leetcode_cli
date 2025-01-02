# leetcode_cli/services/theme_service.py

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
    return conf["theme"]

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

    theme_dir = os.path.join(get_themes_dir(), theme)

    # 1) Load ansi_codes.yaml
    ansi_path = os.path.join(theme_dir, "ansi_codes.yaml")
    if not os.path.exists(ansi_path):
        raise ThemeError(f"File 'ansi_codes.yaml' is missing for theme '{theme}'.")

    try:
        with open(ansi_path, "r", encoding="utf-8") as f:
            ansi_data = yaml.safe_load(f)

        if "ANSI_CODES" not in ansi_data:
            raise ThemeError(f"'ANSI_CODES' missing in ansi_codes.yaml for theme '{theme}'.")

        all_ansi_codes = ansi_data["ANSI_CODES"]

    except yaml.YAMLError as e:
        raise ThemeError(f"File 'ansi_codes.yaml' in theme '{theme}' is not valid YAML: {e}")

    # 2) Load symbols.yaml
    symbols_path = os.path.join(theme_dir, "symbols.yaml")
    if not os.path.exists(symbols_path):
        raise ThemeError(f"File 'symbols.yaml' is missing for theme '{theme}'.")

    try:
        with open(symbols_path, "r", encoding="utf-8") as f:
            sym_data = yaml.safe_load(f)

        if "SYMBOLS" not in sym_data:
            raise ThemeError(f"'SYMBOLS' missing in symbols.yaml for theme '{theme}'.")

        all_symbols = sym_data["SYMBOLS"]

    except yaml.YAMLError as e:
        raise ThemeError(f"File 'symbols.yaml' in theme '{theme}' is not valid YAML: {e}")

    # 3) Load mappings.yaml
    mappings_path = os.path.join(theme_dir, "mappings.yaml")
    if not os.path.exists(mappings_path):
        raise ThemeError(f"File 'mappings.yaml' is missing for theme '{theme}'.")

    try:
        with open(mappings_path, "r", encoding="utf-8") as f:
            all_mappings = yaml.safe_load(f)

        if not isinstance(all_mappings, dict):
            raise ThemeError(f"'mappings.yaml' is valid YAML but not a dictionary for theme '{theme}'.")

    except yaml.YAMLError as e:
        raise ThemeError(f"File 'mappings.yaml' in theme '{theme}' is not valid YAML: {e}")

    # Construct ThemeData
    return ThemeData(
        ANSI_CODES=all_ansi_codes,
        SYMBOLS=all_symbols,
        MAPPINGS=all_mappings
    )

def get_styling(theme_data: ThemeData, category: str, key: str) -> (str, str):
    """
    Returns (ansi_code, symbol) for the given category/key.
    Raises ThemeError if category or key is missing.
    """
    cat_dict = theme_data.MAPPINGS.get(category)
    if cat_dict is None:
        raise ThemeError(f"Category '{category}' not found in MAPPINGS.")

    item = cat_dict.get(key)
    if item is None:
        raise ThemeError(f"Key '{key}' not found in category '{category}'.")

    ansi_chain = item.get("ansi", "")
    symbol_key = item.get("symbol", "")

    resolved_ansi = _resolve_ansi_chain(theme_data.ANSI_CODES, ansi_chain)
    resolved_symbol = _resolve_symbol_chain(theme_data.SYMBOLS, symbol_key)

    return (resolved_ansi, resolved_symbol)

def _resolve_ansi_chain(ansi_codes_dict: dict, chain: str) -> str:
    if not chain:
        return ""

    tokens = [t.strip() for t in chain.split(",")]
    result = ""

    for token in tokens:
        if token not in ansi_codes_dict:
            raise ThemeError(f"Missing ANSI code '{token}' in 'ANSI_CODES'.")

        result += ansi_codes_dict[token]

    return result

def _resolve_symbol_chain(symbols_dict: dict, chain: str) -> str:
    if not chain:
        return ""

    tokens = [t.strip() for t in chain.split(",")]
    result = ""

    for token in tokens:
        if token not in symbols_dict:
            raise ThemeError(f"Missing ANSI code '{token}' in 'ANSI_CODES'.")

        result += symbols_dict[token]

    return result
