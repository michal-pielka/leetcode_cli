import click
from datetime import datetime

from leetcode_cli.services.config_service import get_username
from leetcode_cli.data_fetching.stats_fetcher import fetch_user_stats, fetch_user_activity
from leetcode_cli.parsers.stats_parser import parse_user_stats_data, parse_user_activity_data
from leetcode_cli.formatters.stats_formatter import StatsFormatter
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

    if not include:
        include = ["stats", "calendar"]

    theme_data = load_theme_data()
    formatter = StatsFormatter(theme_data)

    # Fetch and parse stats
    if 'stats' in include:
        stats_data = fetch_user_stats(username)
        click.echo("\n\n")
        click.echo("Fetched stats:")
        click.echo(stats_data)
        click.echo("\n\n")
        if stats_data:
            user_stats = parse_user_stats_data(stats_data)
            formatted_stats = formatter.format_user_stats(user_stats)
            click.echo()
            click.echo(formatted_stats)
            click.echo()
        else:
            click.echo("Error: Failed to fetch stats data.")

    # Fetch and parse activity calendar
    if 'calendar' in include:
        current_year = datetime.now().year
        previous_year = current_year - 1

        activity_current = fetch_user_activity(username, current_year)
        click.echo("\n\n")
        click.echo("Fetched calendar current year:")
        click.echo(activity_current)
        click.echo("\n\n")
        activity_previous = fetch_user_activity(username, previous_year)

        if activity_current and activity_previous:
            user_activity = parse_user_activity_data(activity_previous, activity_current)
            formatted_activity = formatter.format_user_activity(user_activity)
            click.echo()
            click.echo(formatted_activity)
            click.echo()
        else:
            click.echo("Error: Failed to fetch activity data.")
