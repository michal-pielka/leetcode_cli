import os
import logging
import yaml

from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.models.formatting_config import FormattingConfig
from leetcode_cli.exceptions.exceptions import ConfigError

logger = logging.getLogger(__name__)


class FormattingConfigManager:
    """
    Manages loading and processing of formatting configurations.
    """

    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.formatting_config_path = self.get_formatting_config_path()

    def get_formatting_config_path(self) -> str:
        """
        Returns the path to the formatting_config.yaml file.
        """
        config_dir = self.config_manager.config_dir
        return os.path.join(config_dir, "formatting_config.yaml")

    def load_formatting_config(self) -> FormattingConfig:
        """
        Loads the formatting_config.yaml into a FormattingConfig object.

        Returns:
            FormattingConfig: The loaded formatting configuration.

        Raises:
            ConfigError: If the formatting configuration cannot be loaded.
        """
        if not os.path.exists(self.formatting_config_path):
            logger.error(f"Formatting configuration file '{self.formatting_config_path}' not found.")
            raise ConfigError(f"Formatting configuration file '{self.formatting_config_path}' not found.")

        try:
            with open(self.formatting_config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if not isinstance(data, dict):
                    logger.error("Formatting configuration is not a valid YAML dictionary.")
                    raise ConfigError("Invalid formatting configuration format.")

        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error in formatting_config.yaml: {e}")
            raise ConfigError(f"YAML parsing error: {e}")

        except OSError as e:
            logger.error(f"Failed to read formatting_config.yaml: {e}")
            raise ConfigError(f"Failed to read formatting_config.yaml: {e}")

        return FormattingConfig(
            interpretation=data.get("interpretation", {}),
            submission=data.get("submission", {}),
            problem_show=data.get("problem_show", {})
        )
