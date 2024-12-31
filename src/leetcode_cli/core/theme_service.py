# leetcode_cli/core/theme_service.py
import os
import logging
import yaml

from leetcode_cli.core.config_service import load_config, save_config, get_config_path
from leetcode_cli.exceptions.exceptions import ThemeError
from leetcode_cli.models.theme import ThemeData

logger = logging.getLogger(__name__)

def get_themes_dir() -> str:
    """
    Returns the path to the 'themes' directory inside the user's leetcode config folder.
    Typically: ~/.config/leetcode/themes
    """
    config_dir = os.path.dirname(get_config_path())
    return os.path.join(config_dir, "themes")

def list_themes():
    """
    Lists subdirectories in the 'themes' folder, each presumably a theme name.
    """
    themes_dir = get_themes_dir()
    if not os.path.exists(themes_dir):
        return []
    return [d for d in os.listdir(themes_dir) if os.path.isdir(os.path.join(themes_dir, d))]

def get_current_theme() -> str:
    """
    Reads the user's 'theme' from config.json, or returns None if not set.
    """
    conf = load_config()
    return conf.get("theme", None)

def set_current_theme(theme_name: str) -> bool:
    """
    Sets the user's current theme in config.json if it exists in the themes folder.
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

def _load_yaml_file(theme_name: str, filename: str) -> dict:
    """
    Loads a YAML file (e.g. ansi_codes.yaml) from the theme folder and returns its data as a dict.
    Raises ThemeError if file is missing or invalid.
    """
    theme_path = os.path.join(get_themes_dir(), theme_name)
    file_path = os.path.join(theme_path, filename)

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

def load_theme_data() -> ThemeData:
    """
    Loads the theme data from three YAML files:
      - ansi_codes.yaml => Must contain top-level 'ANSI_CODES'
      - symbols.yaml    => Must contain top-level 'SYMBOLS'
      - mappings.yaml   => Contains many subdicts (e.g. INTERPRETATION_ANSI_CODES, etc.)

    Merges them and returns a ThemeData object.
    """
    theme = get_current_theme()
    if not theme:
        raise ThemeError("No theme is set in configuration. (key='theme')")

    # 1) Load ansi_codes.yaml
    ansi_data = _load_yaml_file(theme, "ansi_codes.yaml")
    if "ANSI_CODES" not in ansi_data:
        raise ThemeError(f"'ANSI_CODES' missing in ansi_codes.yaml for theme '{theme}'.")

    # 2) Load symbols.yaml
    sym_data = _load_yaml_file(theme, "symbols.yaml")
    if "SYMBOLS" not in sym_data:
        raise ThemeError(f"'SYMBOLS' missing in symbols.yaml for theme '{theme}'.")

    # 3) Load mappings.yaml
    mappings_data = _load_yaml_file(theme, "mappings.yaml")
    # This should have keys like INTERPRETATION_ANSI_CODES, SUBMISSION_ANSI_CODES, etc.

    # Build a merged dict
    merged = {
        "ANSI_CODES": ansi_data["ANSI_CODES"],
        "SYMBOLS": sym_data["SYMBOLS"],
    }
    for key, val in mappings_data.items():
        merged[key] = val

    # Construct the ThemeData
    return ThemeData(
        ANSI_CODES=merged["ANSI_CODES"],
        SYMBOLS=merged["SYMBOLS"],
        INTERPRETATION_ANSI_CODES=merged.get("INTERPRETATION_ANSI_CODES", {}),
        INTERPRETATION_SYMBOLS=merged.get("INTERPRETATION_SYMBOLS", {}),
        PROBLEMSET_FORMATTER_ANSI_CODES=merged.get("PROBLEMSET_FORMATTER_ANSI_CODES", {}),
        PROBLEMSET_FORMATTER_SYMBOLS=merged.get("PROBLEMSET_FORMATTER_SYMBOLS", {}),
        SUBMISSION_ANSI_CODES=merged.get("SUBMISSION_ANSI_CODES", {}),
        SUBMISSION_SYMBOLS=merged.get("SUBMISSION_SYMBOLS", {}),
        PROBLEM_FORMATTER_ANSI_CODES=merged.get("PROBLEM_FORMATTER_ANSI_CODES", {}),
        PROBLEM_FORMATTER_SYMBOLS=merged.get("PROBLEM_FORMATTER_SYMBOLS", {}),
        STATS_FORMATTER_DIFFICULTY_COLORS=merged.get("STATS_FORMATTER_DIFFICULTY_COLORS", {}),
        STATS_FORMATTER_SYMBOLS=merged.get("STATS_FORMATTER_SYMBOLS", {})
    )

#
# get_symbol(...) and get_ansi_code(...) remain unchanged from your snippet.
# They rely on the final 'ThemeData' merged object.
#

def get_symbol(theme_data: ThemeData, category: str, key: str) -> str:
    """
    Specifically fetch a symbol from e.g. 'INTERPRETATION_SYMBOLS', 'SUBMISSION_SYMBOLS', etc.
    If the symbol references a second-level name in theme_data.SYMBOLS, we resolve that, etc.
    """
    subdict = getattr(theme_data, category)
    if not subdict:
        raise ThemeError(f"ThemeData has no category '{category}' or it's empty.")

    if key not in subdict:
        raise ThemeError(f"Missing key '{key}' in theme category '{category}'.")

    chain = subdict[key]
    return _resolve_symbol_chain(theme_data.SYMBOLS, chain)

def get_ansi_code(theme_data: ThemeData, category: str, key: str) -> str:
    """
    Specifically fetch an ANSI code from e.g. 'SUBMISSION_ANSI_CODES', 'PROBLEM_FORMATTER_ANSI_CODES', etc.
    If multiple tokens are comma-separated, we chain them.
    """
    subdict = getattr(theme_data, category)
    if not subdict:
        raise ThemeError(f"ThemeData has no category '{category}' or it's empty.")

    if key not in subdict:
        raise ThemeError(f"Missing key '{key}' in theme category '{category}'.")

    chain = subdict[key]
    return _resolve_ansi_chain(theme_data.ANSI_CODES, chain)

def _resolve_ansi_chain(ansi_codes_dict: dict, chain: str) -> str:
    """
    Converts a string like "GREEN,BOLD" into the actual ANSI codes by looking up each token.
    """
    if not chain:
        return ""
    tokens = [t.strip() for t in chain.split(',')]
    result = ""
    for token in tokens:
        if token not in ansi_codes_dict:
            raise ThemeError(f"Missing ANSI code '{token}' in 'ANSI_CODES'.")
        result += ansi_codes_dict[token]
    return result

def _resolve_symbol_chain(symbols_dict: dict, chain: str) -> str:
    """
    Similar logic for symbols. If chain is "CHECKMARK" -> "✔", 
    or multiple tokens "CHECKMARK,ATTEMPTED" -> "✔❋" etc.
    """
    if not chain:
        return ""
    tokens = [t.strip() for t in chain.split(',')]
    result = ""
    for token in tokens:
        if token not in symbols_dict:
            raise ThemeError(f"Missing symbol '{token}' in 'SYMBOLS'.")
        result += symbols_dict[token]
    return result
