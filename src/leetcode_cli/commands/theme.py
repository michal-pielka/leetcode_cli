import click
import logging

from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.managers.theme_manager import ThemeManager
from leetcode_cli.exceptions.exceptions import ThemeError, ConfigError

logger = logging.getLogger(__name__)


@click.command(short_help='Change or list themes')
@click.argument('theme_name', required=False)
def theme_cmd(theme_name):
    """
    Show or change the current theme.

    - If THEME_NAME is omitted, list available themes and show the current theme.
    - If THEME_NAME is provided, attempt to set the theme in config.json.
    """
    try:
        # Initialize managers
        config_manager = ConfigManager()
        theme_manager = ThemeManager(config_manager)

        if not theme_name:
            # Display current theme and list available themes
            current = theme_manager.get_current_theme()
            themes = theme_manager.list_themes()

            click.echo(f"Current theme: {current if current else 'None'}")
            click.echo("Available themes:")
            for t in themes:
                click.echo(f"   - {t}")

            return

        # Attempt to set the provided theme
        success = theme_manager.set_current_theme(theme_name)
        if not success:
            click.echo(f"Error: Theme '{theme_name}' not found. Use 'leetcode theme' to list available themes.")
            return

        # Load theme data to validate
        try:
            theme_data = theme_manager.load_theme_data()
            click.echo(f"Theme set to '{theme_name}'.")

        except ThemeError as e:
            click.echo(f"Warning: Theme '{theme_name}' is set, but it seems invalid:\n  {e}\n"
                       "You may need to fix its YAML files or switch to another theme.")

    except (ConfigError, ThemeError) as e:
        logger.error(e)
        click.echo(f"Configuration/Theme Error: {e}", err=True)

    except Exception as e:
        logger.exception("An unexpected error occurred during theme configuration.")
        click.echo("An unexpected error occurred. Please try again.", err=True)
