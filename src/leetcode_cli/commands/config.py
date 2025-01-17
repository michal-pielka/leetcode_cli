import click
import logging

from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.exceptions.exceptions import ConfigError

logger = logging.getLogger(__name__)


@click.command(short_help="Configure user settings")
@click.argument("key", required=False)
@click.argument("value", required=False)
def config_cmd(key, value):
    """
    Configure or view user settings.

    Usage:
      - leetcode config           (shows all config key-value pairs)
      - leetcode config KEY VALUE (sets config KEY to VALUE)

    Valid keys include 'cookie', 'username', and 'language'.
    """
    valid_keys = ["cookie", "username", "language"]

    try:
        config_manager = ConfigManager()

        # If no key was provided, just print out the current config
        if not key:
            click.echo("Current configuration values:")
            for k, v in config_manager.config.items():
                click.echo(f"  {k}: {v}")
            return

        # If user provided a key but it's not valid
        if key not in valid_keys:
            click.echo(
                f"Error: Invalid configuration key '{key}'. "
                f"Valid keys: {', '.join(valid_keys)}"
            )
            return

        # If the user didn't provide a value, show an error
        if value is None:
            click.echo(
                f"Error: You must provide a value for the key '{key}'. Usage: leetcode config {key} SOME_VALUE"
            )
            return

        # Now we handle setting the config
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
