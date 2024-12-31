# leetcode_cli/core/theme_service.py

import os
import json
import logging

from leetcode_cli.core.config_service import load_config, save_config, get_config_path
from leetcode_cli.exceptions.exceptions import ThemeError
from leetcode_cli.models.theme import ThemeData

logger = logging.getLogger(__name__)

def get_themes_dir() -> str:
    config_dir = os.path.dirname(get_config_path())
    return os.path.join(config_dir, "themes")

def list_themes():
    themes_dir = get_themes_dir()
    if not os.path.exists(themes_dir):
        return []
    return [d for d in os.listdir(themes_dir) if os.path.isdir(os.path.join(themes_dir, d))]

def get_current_theme() -> str:
    conf = load_config()
    return conf.get("theme", None)

def set_current_theme(theme_name: str) -> bool:
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
    theme = get_current_theme()
    if not theme:
        raise ThemeError("No theme is set in configuration.")

    ansi_data = _load_json_file(theme, "ansi_codes.json")
    if "ANSI_CODES" not in ansi_data:
        raise ThemeError(f"'ANSI_CODES' missing in ansi_codes.json for theme '{theme}'.")

    sym_data = _load_json_file(theme, "symbols.json")
    if "SYMBOLS" not in sym_data:
        raise ThemeError(f"'SYMBOLS' missing in symbols.json for theme '{theme}'.")

    mappings_data = _load_json_file(theme, "mappings.json")

    # Merge them into a single dict first
    merged = {
        "ANSI_CODES": ansi_data["ANSI_CODES"],
        "SYMBOLS": sym_data["SYMBOLS"],
    }
    for k, v in mappings_data.items():
        merged[k] = v

    # Build a ThemeData object using dict.get(...) for each field
    theme_obj = ThemeData(
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
    return theme_obj

def get_symbol(theme_data: ThemeData, category: str, key: str) -> str:
    """
    Specifically fetch a symbol from the theme data.
    E.g. "CHECKMARK" -> "✔"

    1. We retrieve the first-level mapping from the specified category (like "PROBLEM_FORMATTER_SYMBOLS").
       E.g. 'li' -> "DOT"
    2. If that result is itself a key in theme_data.SYMBOLS, do a second pass.
    3. Otherwise, return it literally.
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
    Specifically fetch an ANSI code from the theme data.
    category might be 'SUBMISSION_ANSI_CODES' or 'PROBLEM_FORMATTER_ANSI_CODES', etc.
    """
    subdict = getattr(theme_data, category)

    if not subdict:
        raise ThemeError(f"ThemeData has no category '{category}' or it's empty.")

    if key not in subdict:
        raise ThemeError(f"Missing key '{key}' in theme category '{category}'.")

    chain = subdict[key]

    return _resolve_ansi_chain(theme_data.ANSI_CODES, chain)



def _load_json_file(theme_name: str, filename: str) -> dict:
    theme_path = os.path.join(get_themes_dir(), theme_name)
    file_path = os.path.join(theme_path, filename)

    if not os.path.exists(file_path):
        raise ThemeError(f"File '{filename}' is missing for theme '{theme_name}'.")

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    except json.JSONDecodeError:
        raise ThemeError(f"File '{filename}' in theme '{theme_name}' is not valid JSON.")

def _resolve_ansi_chain(ansi_codes_dict: dict, chain: str) -> str:
    """
    Converts a chain like "GREEN,BOLD" into the actual ANSI codes by
    looking up each token in ansi_codes_dict.
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
    if not chain:
        return ""

    tokens = [t.strip() for t in chain.split(',')]
    result = ""

    for token in tokens:
        if token not in symbols_dict:
            raise ThemeError(f"Missing ANSI code '{token}' in 'ANSI_CODES'.")

        result += symbols_dict[token]

    return result
