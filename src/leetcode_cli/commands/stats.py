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


@click.command(short_help="Display user statistics from LeetCode")
@click.argument("username", required=False, default=None, metavar="USERNAME")
@click.option(
    "--include",
    "-i",
    multiple=True,
    type=click.Choice(["stats", "calendar"], case_sensitive=False),
    metavar="SECTION",
    help="Sections to display. e.g. --include stats --include calendar",
)
def stats_cmd(username, include):
    """
    Show user stats and/or calendar activity, with color gradients for daily squares.
    """
    try:
        config_manager = ConfigManager()
        auth_service = AuthService(config_manager)
        stats_manager = StatsManager(config_manager, auth_service)
        theme_manager = ThemeManager(config_manager)

        if not username:
            username = config_manager.get_username()
            if not username:
                click.echo("Error: Username not found in config or CLI param.")
                return

        # If user didn’t specify any --include, show both
        if not include:
            include = ("stats", "calendar")

        # 1) Fetch user stats
        try:
            user_stats = stats_manager.get_user_stats(username)
        except StatsError as e:
            click.echo(f"Failed to fetch stats: {e}")
            return

        # 2) Optionally fetch activity calendar
        user_activity = None
        if "calendar" in include:
            try:
                current_year = datetime.now().year
                prev_year = current_year - 1
                user_activity = stats_manager.get_joined_activity(
                    username, prev_year, current_year
                )
            except StatsError as e:
                click.echo(f"Failed to fetch user activity: {e}")
                # we can continue if we want

        # 3) Format the output
        formatter = StatsFormatter(theme_manager)
        final_output_lines = []

        if "stats" in include:
            stats_str = formatter.format_user_stats(user_stats)
            final_output_lines.append(stats_str)

        if "calendar" in include and user_activity:
            cal_str = formatter.format_user_activity(user_activity)
            final_output_lines.append(cal_str)

        # 4) Print
        click.echo("\n\n".join(final_output_lines))

    except (ConfigError, ThemeError, StatsError) as e:
        logger.error(e)
        click.echo(f"Error: {e}", err=True)
    except Exception as e:
        logger.exception("An unexpected error occurred while fetching statistics.")
        click.echo("An unexpected error occurred. Please try again.", err=True)
