# utils/theme_utils.py

import os
import json
import logging
from leetcode_cli.utils.config_utils import get_config_path, _load_config
from leetcode_cli.exceptions.exceptions import ThemeError

# Import the existing required keys from your theme_validation folder.
from leetcode_cli.constants.theme_validation.problem_validation_constants import (
    PROBLEM_FORMATTER_ANSI_CODES_REQUIRED,
    PROBLEM_FORMATTER_SYMBOLS_REQUIRED
)
from leetcode_cli.constants.theme_validation.interpretation_validation_constants import (
    INTERPRETATION_ANSI_CODES_REQUIRED,
    INTERPRETATION_SYMBOLS_REQUIRED
)
from leetcode_cli.constants.theme_validation.submission_validation_constants import (
    SUBMISSION_ANSI_CODES_REQUIRED,
    SUBMISSION_SYMBOLS_REQUIRED
)
from leetcode_cli.constants.theme_validation.problemset_validation_constants import (
    PROBLEMSET_FORMATTER_ANSI_CODES_REQUIRED,
    PROBLEMSET_FORMATTER_SYMBOLS_REQUIRED
)
from leetcode_cli.constants.theme_validation.stats_validation_constants import (
    STATS_FORMATTER_DIFFICULTY_COLORS_REQUIRED,
    STATS_FORMATTER_SYMBOLS_REQUIRED
)

logger = logging.getLogger(__name__)

def get_themes_dir():
    """
    Returns the path to the 'themes' directory,
    which is typically next to config or inside your user config folder, etc.
    """
    config_dir = os.path.dirname(get_config_path())
    return os.path.join(config_dir, "themes")


def list_themes():
    """
    Return a list of all folder names inside the themes directory.
    """
    themes_dir = get_themes_dir()
    if not os.path.exists(themes_dir):
        return []
    return [d for d in os.listdir(themes_dir) if os.path.isdir(os.path.join(themes_dir, d))]


def get_current_theme() -> str:
    """
    Reads user's current theme from config.json.
    Defaults to 'default_theme' if not set.
    """
    config = _load_config()
    theme_name = config.get("theme", "default_theme")
    return theme_name


def set_current_theme(theme_name: str) -> bool:
    """
    Persists the selected theme in config.json,
    but doesn't validate it immediately.
    You can call 'validate_entire_theme()' or 'load_theme_data()'
    afterwards to ensure it's valid.
    """
    available = list_themes()
    if theme_name not in available:
        logger.error(f"Theme '{theme_name}' does not exist in: {available}")
        return False

    # Save it in config
    config = _load_config()
    config["theme"] = theme_name
    from leetcode_cli.utils.config_utils import _save_config
    _save_config(config)

    logger.info(f"Theme set to '{theme_name}'.")
    return True


def _load_json_file(theme_name: str, filename: str) -> dict:
    """
    Loads a JSON file from the user's chosen theme folder.
    Raises ThemeError if missing or invalid.
    """
    theme_path = os.path.join(get_themes_dir(), theme_name)
    file_path = os.path.join(theme_path, filename)

    if not os.path.exists(file_path):
        error_msg = f"File '{filename}' is missing for theme '{theme_name}'."
        logger.error(error_msg)
        raise ThemeError(error_msg)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except json.JSONDecodeError:
        error_msg = f"File '{filename}' in theme '{theme_name}' is not valid JSON."
        logger.error(error_msg)
        raise ThemeError(error_msg)


def load_theme_data() -> dict:
    """
    Unified loading of ALL theme data from three files:
        1) ansi_codes.json → theme_data["ANSI_CODES"]
        2) symbols.json → theme_data["SYMBOLS"]
        3) mappings.json → merges directly
           (e.g. "PROBLEM_FORMATTER_ANSI_CODES", "SUBMISSION_SYMBOLS", etc.)

    After loading, we validate everything and then resolve references.

    If any key is missing, or any reference is invalid,
    we raise ThemeError and do not fallback.
    """
    theme_name = get_current_theme()

    # Load ansi_codes.json
    ansi_data = _load_json_file(theme_name, "ansi_codes.json")
    if "ANSI_CODES" not in ansi_data:
        raise ThemeError(f"'ANSI_CODES' missing in ansi_codes.json for theme '{theme_name}'.")

    # Load symbols.json
    symbols_data = _load_json_file(theme_name, "symbols.json")
    if "SYMBOLS" not in symbols_data:
        raise ThemeError(f"'SYMBOLS' missing in symbols.json for theme '{theme_name}'.")

    # Load mappings.json
    mappings_data = _load_json_file(theme_name, "mappings.json")

    # Merge them all
    theme_data = {
        "ANSI_CODES": ansi_data["ANSI_CODES"],
        "SYMBOLS": symbols_data["SYMBOLS"],
    }
    for k, v in mappings_data.items():
        theme_data[k] = v

    # Validate
    _validate_entire_theme_dict(theme_data, theme_name)

    # Resolve references
    _resolve_all_ansi_and_symbol_refs(theme_data)

    return theme_data


def _validate_entire_theme_dict(theme_data: dict, theme_name: str) -> None:
    """
    Checks that all required sections exist and that all required keys
    are present in each mapping. If anything is missing, raises ThemeError.
    """
    # Check existence of main sections
    if "PROBLEM_FORMATTER_ANSI_CODES" not in theme_data:
        raise ThemeError(f"Missing 'PROBLEM_FORMATTER_ANSI_CODES' in mappings.json for theme '{theme_name}'.")
    if "PROBLEM_FORMATTER_SYMBOLS" not in theme_data:
        raise ThemeError(f"Missing 'PROBLEM_FORMATTER_SYMBOLS' in mappings.json for theme '{theme_name}'.")

    if "INTERPRETATION_ANSI_CODES" not in theme_data:
        raise ThemeError(f"Missing 'INTERPRETATION_ANSI_CODES' in mappings.json for theme '{theme_name}'.")
    if "INTERPRETATION_SYMBOLS" not in theme_data:
        raise ThemeError(f"Missing 'INTERPRETATION_SYMBOLS' in mappings.json for theme '{theme_name}'.")

    if "SUBMISSION_ANSI_CODES" not in theme_data:
        raise ThemeError(f"Missing 'SUBMISSION_ANSI_CODES' in mappings.json for theme '{theme_name}'.")
    if "SUBMISSION_SYMBOLS" not in theme_data:
        raise ThemeError(f"Missing 'SUBMISSION_SYMBOLS' in mappings.json for theme '{theme_name}'.")

    if "PROBLEMSET_FORMATTER_ANSI_CODES" not in theme_data:
        raise ThemeError(f"Missing 'PROBLEMSET_FORMATTER_ANSI_CODES' in mappings.json for theme '{theme_name}'.")
    if "PROBLEMSET_FORMATTER_SYMBOLS" not in theme_data:
        raise ThemeError(f"Missing 'PROBLEMSET_FORMATTER_SYMBOLS' in mappings.json for theme '{theme_name}'.")

    if "STATS_FORMATTER_DIFFICULTY_COLORS" not in theme_data:
        raise ThemeError(f"Missing 'STATS_FORMATTER_DIFFICULTY_COLORS' in mappings.json for theme '{theme_name}'.")
    if "STATS_FORMATTER_SYMBOLS" not in theme_data:
        raise ThemeError(f"Missing 'STATS_FORMATTER_SYMBOLS' in mappings.json for theme '{theme_name}'.")

    # Validate required keys in each subsection

    # Problem
    for req in PROBLEM_FORMATTER_ANSI_CODES_REQUIRED:
        if req not in theme_data["PROBLEM_FORMATTER_ANSI_CODES"]:
            raise ThemeError(f"Missing '{req}' in PROBLEM_FORMATTER_ANSI_CODES for theme '{theme_name}'.")
    for req in PROBLEM_FORMATTER_SYMBOLS_REQUIRED:
        if req not in theme_data["PROBLEM_FORMATTER_SYMBOLS"]:
            raise ThemeError(f"Missing '{req}' in PROBLEM_FORMATTER_SYMBOLS for theme '{theme_name}'.")

    # Interpretation
    for req in INTERPRETATION_ANSI_CODES_REQUIRED:
        if req not in theme_data["INTERPRETATION_ANSI_CODES"]:
            raise ThemeError(f"Missing '{req}' in INTERPRETATION_ANSI_CODES for theme '{theme_name}'.")
    for req in INTERPRETATION_SYMBOLS_REQUIRED:
        if req not in theme_data["INTERPRETATION_SYMBOLS"]:
            raise ThemeError(f"Missing '{req}' in INTERPRETATION_SYMBOLS for theme '{theme_name}'.")

    # Submission
    for req in SUBMISSION_ANSI_CODES_REQUIRED:
        if req not in theme_data["SUBMISSION_ANSI_CODES"]:
            raise ThemeError(f"Missing '{req}' in SUBMISSION_ANSI_CODES for theme '{theme_name}'.")
    for req in SUBMISSION_SYMBOLS_REQUIRED:
        if req not in theme_data["SUBMISSION_SYMBOLS"]:
            raise ThemeError(f"Missing '{req}' in SUBMISSION_SYMBOLS for theme '{theme_name}'.")

    # Problemset
    for req in PROBLEMSET_FORMATTER_ANSI_CODES_REQUIRED:
        if req not in theme_data["PROBLEMSET_FORMATTER_ANSI_CODES"]:
            raise ThemeError(f"Missing '{req}' in PROBLEMSET_FORMATTER_ANSI_CODES for theme '{theme_name}'.")
    for req in PROBLEMSET_FORMATTER_SYMBOLS_REQUIRED:
        if req not in theme_data["PROBLEMSET_FORMATTER_SYMBOLS"]:
            raise ThemeError(f"Missing '{req}' in PROBLEMSET_FORMATTER_SYMBOLS for theme '{theme_name}'.")

    # Stats
    for req in STATS_FORMATTER_DIFFICULTY_COLORS_REQUIRED:
        if req not in theme_data["STATS_FORMATTER_DIFFICULTY_COLORS"]:
            raise ThemeError(f"Missing '{req}' in STATS_FORMATTER_DIFFICULTY_COLORS for theme '{theme_name}'.")
    for req in STATS_FORMATTER_SYMBOLS_REQUIRED:
        if req not in theme_data["STATS_FORMATTER_SYMBOLS"]:
            raise ThemeError(f"Missing '{req}' in STATS_FORMATTER_SYMBOLS for theme '{theme_name}'.")


def _resolve_all_ansi_and_symbol_refs(theme_data: dict):
    """
    Replace references in each mapping sub-dict with the actual ANSI codes or symbols
    from theme_data["ANSI_CODES"] and theme_data["SYMBOLS"].

    If something is not found, raise ThemeError. We do not fallback.
    """

    def resolve_ansi(mapping_dict):
        for key, value in mapping_dict.items():
            # e.g. "GREEN BOLD" → ["GREEN", "BOLD"]
            parts = value.split()
            combined = ""
            for part in parts:
                if part not in theme_data["ANSI_CODES"]:
                    raise ThemeError(
                        f"ANSI code '{part}' (used in key '{key}') not found in 'ANSI_CODES'."
                    )
                combined += theme_data["ANSI_CODES"][part]
            mapping_dict[key] = combined

    def resolve_symbols(mapping_dict):
        for key, value in mapping_dict.items():
            # e.g. "CHECKMARK" → "✔"
            if value not in theme_data["SYMBOLS"]:
                raise ThemeError(
                    f"Symbol '{value}' (used in key '{key}') not found in 'SYMBOLS'."
                )
            mapping_dict[key] = theme_data["SYMBOLS"][value]

    # Problem
    resolve_ansi(theme_data["PROBLEM_FORMATTER_ANSI_CODES"])
    resolve_symbols(theme_data["PROBLEM_FORMATTER_SYMBOLS"])
    # Interpretation
    resolve_ansi(theme_data["INTERPRETATION_ANSI_CODES"])
    resolve_symbols(theme_data["INTERPRETATION_SYMBOLS"])
    # Submission
    resolve_ansi(theme_data["SUBMISSION_ANSI_CODES"])
    resolve_symbols(theme_data["SUBMISSION_SYMBOLS"])
    # Problemset
    resolve_ansi(theme_data["PROBLEMSET_FORMATTER_ANSI_CODES"])
    resolve_symbols(theme_data["PROBLEMSET_FORMATTER_SYMBOLS"])
    # Stats
    resolve_ansi(theme_data["STATS_FORMATTER_DIFFICULTY_COLORS"])
    resolve_symbols(theme_data["STATS_FORMATTER_SYMBOLS"])


def validate_entire_theme() -> None:
    """
    Convenience function that attempts to load and validate the entire theme.
    If anything fails, a ThemeError is raised.
    """
    load_theme_data()  # just load, which triggers validation and resolution
