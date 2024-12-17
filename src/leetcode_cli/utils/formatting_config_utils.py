import json
import os

from leetcode_cli.utils.config_utils import get_config_path
from leetcode_cli.constants.formatting_config_constants import DEFAULT_FORMATTING_CONFIG

def load_formatting_config() -> dict:
    config_dir = os.path.dirname(get_config_path())
    formatting_config_path = os.path.join(config_dir, "formatting_config.json")

    if not os.path.exists(formatting_config_path):
        # Create with defaults
        with open(formatting_config_path, "w") as f:
            json.dump(DEFAULT_FORMATTING_CONFIG, f, indent=4)

        return DEFAULT_FORMATTING_CONFIG

    try:
        with open(formatting_config_path, "r") as f:
            user_config = json.load(f)
            return _merge_dicts(DEFAULT_FORMATTING_CONFIG, user_config)

    except (json.JSONDecodeError, OSError) as e:
        return DEFAULT_FORMATTING_CONFIG


def _merge_dicts(defaults, user_config):
    for key, value in defaults.items():
        if key in user_config:
            if isinstance(value, dict) and isinstance(user_config[key], dict):
                _merge_dicts(value, user_config[key])

            else:
                defaults[key] = user_config[key]

    return defaults

