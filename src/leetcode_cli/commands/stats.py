
# leetcode_cli/commands/stats.py
import click
from datetime import datetime
from leetcode_cli.utils.user_utils import get_username
from leetcode_cli.data_fetching.stats_fetcher import fetch_user_stats, fetch_user_activity
from leetcode_cli.parsers.stats_parser import get_formatted_leetcode_stats, get_formatted_daily_activity
from leetcode_cli.parsers.parser_utils.stats_parser_utils import join_and_slice_calendars, fill_daily_activity
from leetcode_cli.graphics.escape_sequences import ANSI_RESET, ANSI_CODES

@click.command(short_help='Display user stats')
@click.argument('username', required=False, default=get_username())
@click.option('--include', multiple=True,
    type=click.Choice(["stats", "calendar"], case_sensitive=False),
    help='Sections to display (default: all).')
def stats_cmd(username, include):
    """
    Display LeetCode user statistics.
    """
    if not username:
        click.echo(f"Error: Username not set. Use 'leetcode config username <user>'.")
        return

    if not include:
        include = ["stats", "calendar"]

    if 'stats' in include:
        stats_data = fetch_user_stats(username)
        if stats_data:
            formatted_stats = get_formatted_leetcode_stats(stats_data)
            click.echo(formatted_stats)
        else:
            click.echo("Error: Failed to fetch stats.")

    if 'calendar' in include:
        current_year = datetime.now().year
        prev_year = current_year - 1
        activity_current = fetch_user_activity(username, current_year)
        activity_previous = fetch_user_activity(username, prev_year)

        if activity_current and activity_previous:
            joined = join_and_slice_calendars(activity_previous, activity_current)
            filled = fill_daily_activity(joined)
            formatted_activity = get_formatted_daily_activity(filled)
            click.echo(formatted_activity)
        else:
            click.echo("Error: Failed to fetch user activity.")
