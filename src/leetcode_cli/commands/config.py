import click
import logging

from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.exceptions.exceptions import ConfigError

logger = logging.getLogger(__name__)


@click.command(short_help="Configure user settings")
@click.argument("key")
@click.argument("value")
def config_cmd(key, value):
    """
    Configure user settings.

    KEY can be 'cookie', 'username', or 'language'.
    """
    valid_keys = ["cookie", "username", "language"]

    if key not in valid_keys:
        click.echo(
            f"Error: Invalid configuration key '{key}'. Valid keys: {', '.join(valid_keys)}"
        )
        return

    try:
        # Initialize ConfigManager
        config_manager = ConfigManager()

        if key == "cookie":
            config_manager.set_cookie(value)
            click.echo("Cookie set successfully.")

        elif key == "username":
            config_manager.set_username(value)
            click.echo(f"Username set to '{value}'.")

        elif key == "language":
            config_manager.set_language(value)
            click.echo(f"Language set to '{value}'.")

    except ConfigError as e:
        logger.error(e)
        click.echo(f"Configuration Error: {e}", err=True)

    except Exception as e:
        logger.exception("An unexpected error occurred during configuration.")
        click.echo("An unexpected error occurred. Please try again.", err=True)
