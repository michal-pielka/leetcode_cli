import os
import logging
import yaml

from leetcode_cli.services.config_service import get_config_dir
from leetcode_cli.models.formatting_config import FormattingConfig

logger = logging.getLogger(__name__)

def load_formatting_config() -> FormattingConfig:
    """
    Load ~/.config/leetcode/formatting_config.yaml into a FormattingConfig object.
    """
    formatting_path = os.path.join(get_config_dir(), "formatting_config.yaml")

    with open(formatting_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return FormattingConfig(
        interpretation=data.get("interpretation", {}),
        submission=data.get("submission", {}),
        problem_show=data.get("problem_show", {})
    )
