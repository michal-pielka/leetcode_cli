
# leetcode_cli/commands/download_problems.py
import click
import json
import os
from leetcode_cli.data_fetching.problemset_fetcher import fetch_problemset
from leetcode_cli.utils.user_utils import get_problems_data_path
from leetcode_cli.utils.user_utils import save_problems_data

@click.command(short_help='Download all problems metadata')
def download_problems_cmd():
    """
    Download all LeetCode problems metadata and save locally.
    """
    problems_data = fetch_problemset(cookie=None, csrf_token=None, tags=None, difficulty=None, limit=100000, skip=0)
    if not problems_data:
        click.echo("Error: Failed to fetch problems metadata.")
        return

    save_problems_data(problems_data)
    problems_path = get_problems_data_path()
    click.echo(f"Problems metadata downloaded to '{problems_path}'.")
