# leetcode_cli/commands/stats.py
import click
from datetime import datetime
from leetcode_cli.utils.config_utils import get_username
from leetcode_cli.data_fetching.stats_fetcher import fetch_user_stats, fetch_user_activity
from leetcode_cli.parsers.stats_parser import parse_user_stats_data, parse_user_activity_data
from leetcode_cli.formatters.stats_formatter import format_user_stats, format_user_activity

@click.command(short_help='Display user stats')
@click.argument('username', required=False, default=get_username())
@click.option(
    '--include',
    multiple=True,
    type=click.Choice(["stats", "calendar"], case_sensitive=False),
    help='Sections to display (default: all). Options: stats, calendar'
)
def stats_cmd(username, include):
    """
    Display LeetCode user statistics.

    Usage:
        leetcode stats
        leetcode stats USERNAME
    """
    if not username:
        click.echo("Error: Username not set. Use 'leetcode config username <user>'.")
        return

    if not include:
        include = ["stats", "calendar"]

    # Fetch and parse stats
    if 'stats' in include:
        stats_data = fetch_user_stats(username)
        if stats_data:
            user_stats = parse_user_stats_data(stats_data)
            formatted_stats = format_user_stats(user_stats)
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
        activity_previous = fetch_user_activity(username, previous_year)

        if activity_current and activity_previous:
            user_activity = parse_user_activity_data(activity_previous, activity_current)
            formatted_activity = format_user_activity(user_activity)
            click.echo()
            click.echo(formatted_activity)
            click.echo()
        else:
            click.echo("Error: Failed to fetch activity data.")
