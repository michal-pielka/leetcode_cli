# file: commands/stats.py

import click
import logging
from datetime import datetime

from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.managers.auth_service import AuthService
from leetcode_cli.managers.stats_manager import StatsManager
from leetcode_cli.managers.theme_manager import ThemeManager
from leetcode_cli.managers.formatting_config_manager import FormattingConfigManager

from leetcode_cli.formatters.stats_data_formatter import StatsFormatter
from leetcode_cli.exceptions.exceptions import ConfigError, StatsError, ThemeError

logger = logging.getLogger(__name__)

@click.command(short_help='Display user statistics from LeetCode')
@click.argument('username', required=False, default=None, metavar='USERNAME')
@click.option(
    '--include', '-i',
    multiple=True,
    type=click.Choice(["stats", "calendar"], case_sensitive=False),
    metavar='SECTION',
    help='Sections to display. Overrides formatting_config.'
)
def stats_cmd(username, include):
    """
    Show user stats and/or calendar activity. For example:
      leetcode stats <username> --include stats --include calendar
    """
    try:
        config_manager = ConfigManager()
        auth_service = AuthService(config_manager)
        stats_manager = StatsManager(config_manager, auth_service)
        theme_manager = ThemeManager(config_manager)
        formatting_config_manager = FormattingConfigManager(config_manager)

        # Possibly load formatting_config if the StatsFormatter uses it—(some do, some don't).
        # e.g., if you have "stats_show" or something. We'll skip that for now.

        if not username:
            username = config_manager.get_username()
            if not username:
                click.echo("Error: Username not found in config or CLI param.")
                return

        # If user didn't specify, show both
        if not include:
            include = ("stats", "calendar")

        # Create a StatsFormatter for final output
        formatter = StatsFormatter(theme_manager)

        if 'stats' in include:
            try:
                user_stats = stats_manager.get_user_stats(username)
                formatted_stats = formatter.format_user_stats(user_stats)
                click.echo()
                click.echo(formatted_stats)
                click.echo()
            except StatsError as e:
                logger.error(f"Failed to fetch user stats: {e}")
                click.echo(f"Error: {e}")

        if 'calendar' in include:
            try:
                current_year = datetime.now().year
                prev_year = current_year - 1
                user_activity = stats_manager.get_joined_activity(
                    username, prev_year, current_year
                )
                formatted_calendar = formatter.format_user_activity(user_activity)
                click.echo()
                click.echo(formatted_calendar)
                click.echo()
            except StatsError as e:
                logger.error(f"Failed to fetch user activity: {e}")
                click.echo(f"Error: {e}")

    except (ConfigError, ThemeError, StatsError) as e:
        logger.error(e)
        click.echo(f"Error: {e}", err=True)
    except Exception as e:
        logger.exception("An unexpected error occurred while fetching statistics.")
        click.echo("An unexpected error occurred. Please try again.", err=True)
