import json
import os
import logging

from leetcode_cli.core.config_service import get_config_dir
from leetcode_cli.models.formatting_config import FormattingConfig

logger = logging.getLogger(__name__)

def load_formatting_config() -> FormattingConfig:
    formatting_path = os.path.join(get_config_dir(), "formatting_config.json")

    with open(formatting_path, "r", encoding="utf-8") as f:
        user_data = json.load(f)

    return FormattingConfig(
        interpretation=user_data["interpretation"],
        submission=user_data["submission"],
        problem_show=user_data["problem_show"]
    )

