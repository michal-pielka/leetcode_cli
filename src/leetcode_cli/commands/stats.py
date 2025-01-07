import click
import logging
from datetime import datetime

from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.managers.stats_manager import StatsManager
from leetcode_cli.formatters.stats_data_formatter import StatsFormatter
from leetcode_cli.managers.theme_manager import ThemeManager
from leetcode_cli.data_fetchers.stats_data_fetcher import fetch_user_stats, fetch_user_activity
from leetcode_cli.parsers.stats_data_parser import parse_user_stats_data, parse_user_activity_data
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
    try:
        config_manager = ConfigManager()
        stats_manager = StatsManager()
        theme_manager = ThemeManager(config_manager)
        formatter = StatsFormatter(theme_manager)

        if not username:
            username = config_manager.get_username()
            if not username:
                click.echo("Error: Username not found in config.")
                return

        if not include:
            include = ["stats", "calendar"]

        # --stats
        if 'stats' in include:
            try:
                stats_data = fetch_user_stats(username)
                if stats_data:
                    user_stats = parse_user_stats_data(stats_data)
                    formatted_stats = formatter.format_user_stats(user_stats)
                    click.echo()
                    click.echo(formatted_stats)
                    click.echo()
                else:
                    click.echo("Error: Failed to fetch stats data.")
            except Exception as e:
                logger.error(f"Failed to fetch or parse stats data: {e}")
                click.echo(f"Error: {e}")

        # --calendar
        if 'calendar' in include:
            try:
                current_year = datetime.now().year
                prev_year = current_year - 1

                activity_current = fetch_user_activity(username, current_year)
                activity_previous = fetch_user_activity(username, prev_year)

                if activity_current and activity_previous:
                    # Parse user activity into a model
                    activity_model = parse_user_activity_data(activity_previous, activity_current)
                    # Now pass the model to the formatter
                    formatted_activity = formatter.format_user_activity(activity_model)
                    click.echo()
                    click.echo(formatted_activity)
                    click.echo()
                else:
                    click.echo("Error: Failed to fetch activity data.")
            except Exception as e:
                logger.error(f"Failed to fetch or parse activity data: {e}")
                click.echo(f"Error: {e}")

    except (ConfigError, ThemeError, StatsError) as e:
        logger.error(e)
        click.echo(f"Error: {e}", err=True)
    except Exception as e:
        logger.exception("An unexpected error occurred while fetching statistics.")
        click.echo("An unexpected error occurred. Please try again.", err=True)
