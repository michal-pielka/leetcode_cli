import os
import json
import logging
from leetcode_cli.utils.config_utils import get_config_path, _load_config, _save_config
from leetcode_cli.constants.default_theme_constants import DEFAULT_THEME_FILES
from leetcode_cli.exceptions.exceptions import ThemeError

# Import validation constants
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
    config_dir = os.path.dirname(get_config_path())
    return os.path.join(config_dir, "themes")

def list_themes():
    themes_dir = get_themes_dir()
    if not os.path.exists(themes_dir):
        return []
    return [d for d in os.listdir(themes_dir) if os.path.isdir(os.path.join(themes_dir, d))]

def set_current_theme(theme_name):
    available_themes = list_themes()
    if theme_name not in available_themes:
        logger.error(f"Theme '{theme_name}' does not exist.")
        return False

    config = _load_config()
    config["theme"] = theme_name
    _save_config(config)
    logger.info(f"Theme set to '{theme_name}'.")
    return True

def get_current_theme() -> str:
    config = _load_config()
    theme_name = config.get("theme", "default_theme")
    if not theme_name:
        logger.debug("Theme not set in config, using 'default_theme'.")
        theme_name = "default_theme"
    return theme_name

def initialize_config_and_default_theme():
    config_path = get_config_path()
    config_dir = os.path.dirname(config_path)
    themes_dir = os.path.join(config_dir, "themes")
    default_theme_dir = os.path.join(themes_dir, "default_theme")

    if not os.path.exists(config_dir):
        os.makedirs(config_dir, exist_ok=True)
        logger.info(f"Created configuration directory at '{config_dir}'.")

    if not os.path.exists(themes_dir):
        os.makedirs(themes_dir, exist_ok=True)
        logger.info(f"Created themes directory at '{themes_dir}'.")

    if not os.path.exists(default_theme_dir):
        os.makedirs(default_theme_dir, exist_ok=True)
        for filename, data in DEFAULT_THEME_FILES.items():
            file_path = os.path.join(default_theme_dir, filename)
            with open(file_path, "w") as f:
                json.dump(data, f, indent=4)
        logger.info(f"Default theme created at '{default_theme_dir}'.")


### Generic Loading and Validation ###

def _load_json_file(theme_name, filename):
    theme_path = os.path.join(get_themes_dir(), theme_name)
    file_path = os.path.join(theme_path, filename)

    if not os.path.exists(file_path):
        error_msg = f"'{filename}' file is missing for theme '{theme_name}'."
        logger.error(error_msg)
        raise ThemeError(error_msg)

    try:
        with open(file_path, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        error_msg = f"'{filename}' in theme '{theme_name}' is not valid JSON."
        logger.error(error_msg)
        raise ThemeError(error_msg)

    return data

def _resolve_ansi_refs(mapping_dict, ansi_codes, theme_name):
    for k, v in mapping_dict.items():
        if isinstance(v, str):
            parts = v.split()
            combined_code = ""
            for part in parts:
                code = ansi_codes.get(part)
                if code is None:
                    error_msg = f"ANSI code '{part}' referenced in '{k}' not found in 'ANSI_CODES' for theme '{theme_name}'."
                    logger.error(error_msg)
                    raise ThemeError(error_msg)
                combined_code += code
            mapping_dict[k] = combined_code

def _resolve_symbol_refs(mapping_dict, symbols, theme_name):
    for k, v in mapping_dict.items():
        if isinstance(v, str):
            symbol_code = symbols.get(v)
            if symbol_code is None:
                error_msg = f"Symbol '{v}' referenced in '{k}' not found in 'SYMBOLS' for theme '{theme_name}'."
                logger.error(error_msg)
                raise ThemeError(error_msg)
            mapping_dict[k] = symbol_code

def _load_ansi_symbols(theme_name):
    ansi_data = _load_json_file(theme_name, "ansi_codes.json")
    symbols_data = _load_json_file(theme_name, "symbols.json")

    if "ANSI_CODES" not in ansi_data:
        raise ThemeError(f"Missing 'ANSI_CODES' in ansi_codes.json for theme '{theme_name}'.")
    if "SYMBOLS" not in symbols_data:
        raise ThemeError(f"Missing 'SYMBOLS' in symbols.json for theme '{theme_name}'.")

    theme_data = {
        "ANSI_CODES": ansi_data["ANSI_CODES"],
        "SYMBOLS": symbols_data["SYMBOLS"]
    }
    return theme_data


### Validation Functions for Each Mappings File ###

def validate_problem_mappings(theme_data, theme_name):
    if "PROBLEM_FORMATTER_ANSI_CODES" not in theme_data:
        raise ThemeError(f"Missing 'PROBLEM_FORMATTER_ANSI_CODES' in problem_mappings.json for theme '{theme_name}'.")

    if "PROBLEM_FORMATTER_SYMBOLS" not in theme_data:
        raise ThemeError(f"Missing 'PROBLEM_FORMATTER_SYMBOLS' in problem_mappings.json for theme '{theme_name}'.")

    for key in PROBLEM_FORMATTER_ANSI_CODES_REQUIRED:
        if key not in theme_data["PROBLEM_FORMATTER_ANSI_CODES"]:
            raise ThemeError(f"Missing '{key}' in PROBLEM_FORMATTER_ANSI_CODES for theme '{theme_name}'.")

    for key in PROBLEM_FORMATTER_SYMBOLS_REQUIRED:
        if key not in theme_data["PROBLEM_FORMATTER_SYMBOLS"]:
            raise ThemeError(f"Missing '{key}' in PROBLEM_FORMATTER_SYMBOLS for theme '{theme_name}'.")


def validate_interpretation_mappings(theme_data, theme_name):
    if "INTERPRETATION_ANSI_CODES" not in theme_data:
        raise ThemeError(f"Missing 'INTERPRETATION_ANSI_CODES' in interpretation_mappings.json for theme '{theme_name}'.")
    if "INTERPRETATION_SYMBOLS" not in theme_data:
        raise ThemeError(f"Missing 'INTERPRETATION_SYMBOLS' in interpretation_mappings.json for theme '{theme_name}'.")

    for key in INTERPRETATION_ANSI_CODES_REQUIRED:
        if key not in theme_data["INTERPRETATION_ANSI_CODES"]:
            raise ThemeError(f"Missing '{key}' in INTERPRETATION_ANSI_CODES for theme '{theme_name}'.")

    for key in INTERPRETATION_SYMBOLS_REQUIRED:
        if key not in theme_data["INTERPRETATION_SYMBOLS"]:
            raise ThemeError(f"Missing '{key}' in INTERPRETATION_SYMBOLS for theme '{theme_name}'.")


def validate_submission_mappings(theme_data, theme_name):
    if "SUBMISSION_ANSI_CODES" not in theme_data:
        raise ThemeError(f"Missing 'SUBMISSION_ANSI_CODES' in submission_mappings.json for theme '{theme_name}'.")
    if "SUBMISSION_SYMBOLS" not in theme_data:
        raise ThemeError(f"Missing 'SUBMISSION_SYMBOLS' in submission_mappings.json for theme '{theme_name}'.")

    for key in SUBMISSION_ANSI_CODES_REQUIRED:
        if key not in theme_data["SUBMISSION_ANSI_CODES"]:
            raise ThemeError(f"Missing '{key}' in SUBMISSION_ANSI_CODES for theme '{theme_name}'.")

    for key in SUBMISSION_SYMBOLS_REQUIRED:
        if key not in theme_data["SUBMISSION_SYMBOLS"]:
            raise ThemeError(f"Missing '{key}' in SUBMISSION_SYMBOLS for theme '{theme_name}'.")


def validate_problemset_mappings(theme_data, theme_name):
    if "PROBLEMSET_FORMATTER_ANSI_CODES" not in theme_data:
        raise ThemeError(f"Missing 'PROBLEMSET_FORMATTER_ANSI_CODES' in problemset_mappings.json for theme '{theme_name}'.")
    if "PROBLEMSET_FORMATTER_SYMBOLS" not in theme_data:
        raise ThemeError(f"Missing 'PROBLEMSET_FORMATTER_SYMBOLS' in problemset_mappings.json for theme '{theme_name}'.")

    for key in PROBLEMSET_FORMATTER_ANSI_CODES_REQUIRED:
        if key not in theme_data["PROBLEMSET_FORMATTER_ANSI_CODES"]:
            raise ThemeError(f"Missing '{key}' in PROBLEMSET_FORMATTER_ANSI_CODES for theme '{theme_name}'.")

    for key in PROBLEMSET_FORMATTER_SYMBOLS_REQUIRED:
        if key not in theme_data["PROBLEMSET_FORMATTER_SYMBOLS"]:
            raise ThemeError(f"Missing '{key}' in PROBLEMSET_FORMATTER_SYMBOLS for theme '{theme_name}'.")


def validate_stats_mappings(theme_data, theme_name):
    if "STATS_FORMATTER_DIFFICULTY_COLORS" not in theme_data:
        raise ThemeError(f"Missing 'STATS_FORMATTER_DIFFICULTY_COLORS' in stats_mappings.json for theme '{theme_name}'.")
    if "STATS_FORMATTER_SYMBOLS" not in theme_data:
        raise ThemeError(f"Missing 'STATS_FORMATTER_SYMBOLS' in stats_mappings.json for theme '{theme_name}'.")

    for key in STATS_FORMATTER_DIFFICULTY_COLORS_REQUIRED:
        if key not in theme_data["STATS_FORMATTER_DIFFICULTY_COLORS"]:
            raise ThemeError(f"Missing '{key}' in STATS_FORMATTER_DIFFICULTY_COLORS for theme '{theme_name}'.")

    for key in STATS_FORMATTER_SYMBOLS_REQUIRED:
        if key not in theme_data["STATS_FORMATTER_SYMBOLS"]:
            raise ThemeError(f"Missing '{key}' in STATS_FORMATTER_SYMBOLS for theme '{theme_name}'.")


### Partial Loading Functions ###

def load_problem_theme_data():
    theme_name = get_current_theme()
    theme_data = _load_ansi_symbols(theme_name)
    problem_mappings = _load_json_file(theme_name, "problem_mappings.json")
    theme_data.update(problem_mappings)
    validate_problem_mappings(theme_data, theme_name)
    _resolve_ansi_refs(theme_data["PROBLEM_FORMATTER_ANSI_CODES"], theme_data["ANSI_CODES"], theme_name)
    _resolve_symbol_refs(theme_data["PROBLEM_FORMATTER_SYMBOLS"], theme_data["SYMBOLS"], theme_name)
    return theme_data

def load_interpretation_theme_data():
    theme_name = get_current_theme()
    theme_data = _load_ansi_symbols(theme_name)
    interpretation_mappings = _load_json_file(theme_name, "interpretation_mappings.json")
    theme_data.update(interpretation_mappings)
    validate_interpretation_mappings(theme_data, theme_name)
    _resolve_ansi_refs(theme_data["INTERPRETATION_ANSI_CODES"], theme_data["ANSI_CODES"], theme_name)
    _resolve_symbol_refs(theme_data["INTERPRETATION_SYMBOLS"], theme_data["SYMBOLS"], theme_name)
    return theme_data

def load_submission_theme_data():
    theme_name = get_current_theme()
    theme_data = _load_ansi_symbols(theme_name)
    submission_mappings = _load_json_file(theme_name, "submission_mappings.json")
    theme_data.update(submission_mappings)
    validate_submission_mappings(theme_data, theme_name)
    _resolve_ansi_refs(theme_data["SUBMISSION_ANSI_CODES"], theme_data["ANSI_CODES"], theme_name)
    _resolve_symbol_refs(theme_data["SUBMISSION_SYMBOLS"], theme_data["SYMBOLS"], theme_name)
    return theme_data

def load_problemset_theme_data():
    theme_name = get_current_theme()
    theme_data = _load_ansi_symbols(theme_name)
    problemset_mappings = _load_json_file(theme_name, "problemset_mappings.json")
    theme_data.update(problemset_mappings)
    validate_problemset_mappings(theme_data, theme_name)
    _resolve_ansi_refs(theme_data["PROBLEMSET_FORMATTER_ANSI_CODES"], theme_data["ANSI_CODES"], theme_name)
    _resolve_symbol_refs(theme_data["PROBLEMSET_FORMATTER_SYMBOLS"], theme_data["SYMBOLS"], theme_name)
    return theme_data

def load_stats_theme_data():
    theme_name = get_current_theme()
    theme_data = _load_ansi_symbols(theme_name)
    stats_mappings = _load_json_file(theme_name, "stats_mappings.json")
    theme_data.update(stats_mappings)
    validate_stats_mappings(theme_data, theme_name)
    _resolve_ansi_refs(theme_data["STATS_FORMATTER_DIFFICULTY_COLORS"], theme_data["ANSI_CODES"], theme_name)
    _resolve_symbol_refs(theme_data["STATS_FORMATTER_SYMBOLS"], theme_data["SYMBOLS"], theme_name)
    return theme_data


### New: Validate the Entire Theme ###

def validate_entire_theme():
    """
    Attempts to load and validate all theme mappings for the current theme.
    If any partial load or validation fails, raises ThemeError.
    """
    load_problem_theme_data()          # Validates problem_mappings.json
    load_interpretation_theme_data()   # Validates interpretation_mappings.json
    load_submission_theme_data()       # Validates submission_mappings.json
    load_problemset_theme_data()       # Validates problemset_mappings.json
    load_stats_theme_data()            # Validates stats_mappings.json
