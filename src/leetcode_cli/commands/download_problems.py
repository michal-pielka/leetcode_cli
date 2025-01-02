import click
from leetcode_cli.data_fetchers.problemset_fetcher import fetch_problemset
from leetcode_cli.services.problemset_service import get_problems_data_path, save_problemset_metadata

@click.command(short_help='Download all problems metadata')
def download_problems_cmd():
    """
    Download all LeetCode problems metadata and save locally (problems_metadata.json).
    """
    problems_data = fetch_problemset(
        cookie=None,
        csrf_token=None,
        tags=None,
        difficulty=None,
        limit=100000,
        skip=0
    )
    if not problems_data:
        click.echo("Error: Failed to fetch problems metadata.")
        return

    save_problemset_metadata(problems_data)
    problems_path = get_problems_data_path()
    click.echo(f"Problems metadata downloaded to '{problems_path}'.")
