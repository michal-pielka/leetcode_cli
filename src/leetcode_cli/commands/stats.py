import click
from datetime import datetime

from leetcode_cli.services.config_service import get_username
from leetcode_cli.data_fetchers.stats_data_fetcher import fetch_user_stats, fetch_user_activity
from leetcode_cli.parsers.stats_data_parser import parse_user_stats_data, parse_user_activity_data
from leetcode_cli.formatters.stats_data_formatter import StatsFormatter
from leetcode_cli.services.theme_service import load_theme_data

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
    Display LeetCode user statistics.

    Usage:
        leetcode stats
        leetcode stats USERNAME
    """
    if not username:
        username = get_username()

        if not username:
            click.echo("Error: Username not found in config, use leetcode config username USERNAME or leetcode stats USERNAME")

    if not include:
        include = ["stats", "calendar"]

    theme_data = load_theme_data()
    formatter = StatsFormatter(theme_data)

    if 'stats' in include:
        stats_data = fetch_user_stats(username)
        if stats_data:
            user_stats = parse_user_stats_data(stats_data)
            formatted_stats = formatter.format_user_stats(user_stats)
            click.echo()
            click.echo(formatted_stats)
            click.echo()
        else:
            click.echo("Error: Failed to fetch stats data.")

    if 'calendar' in include:
        current_year = datetime.now().year
        previous_year = current_year - 1

        activity_current = fetch_user_activity(username, current_year)
        activity_previous = fetch_user_activity(username, previous_year)

        if activity_current and activity_previous:
            user_activity = parse_user_activity_data(activity_previous, activity_current)
            formatted_activity = formatter.format_user_activity(user_activity)
            click.echo()
            click.echo(formatted_activity)
            click.echo()
        else:
            click.echo("Error: Failed to fetch activity data.")
