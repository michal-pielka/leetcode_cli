# leetcode_cli/commands/list_problems.py
import click

from leetcode_cli.utils.config_utils import get_cookie, extract_csrf_token
from leetcode_cli.utils.download_problems_utils import load_problems_metadata, filter_problems
from leetcode_cli.data_fetching.problemset_fetcher import fetch_problemset
from leetcode_cli.parsers.problemset_data_parser import parse_problemset_data
from leetcode_cli.formatters.problemset_formatter import ProblemSetFormatter
from leetcode_cli.constants.problem_constants import POSSIBLE_TAGS

def validate_positive_integer(ctx, param, value):
    if value <= 0:
        raise click.BadParameter('Must be greater than 0.')
    return value

@click.command(short_help='List problems')
@click.option('--difficulty', type=click.Choice(["EASY", "MEDIUM", "HARD"], case_sensitive=False), help='Filter by difficulty (default: all difficulties).')
@click.option('--tag', multiple=True, type=click.Choice(POSSIBLE_TAGS, case_sensitive=False), help='Filter by tag (default: all tags).')
@click.option('--limit', type=int, default=50, callback=validate_positive_integer, help='Limit results (default: 50)')
@click.option('--page', type=int, default=1, callback=validate_positive_integer, help='Page number (default: 1)')
@click.option('--use-downloaded', is_flag=True, help='Use downloaded problems metadata.')
def list_cmd(difficulty, tag, limit, page, use_downloaded):
    """List LeetCode problems with optional filters."""
    skip = (page - 1) * limit

    if use_downloaded:
        problems_data = load_problems_metadata()
        if not problems_data:
            click.echo("No local metadata found. Use 'leetcode download_problems' first.")
            return

        filtered_problems = filter_problems(problems_data, difficulty, tag)
        if not filtered_problems:
            click.echo("No problems found with these filters.")
            return

        if skip >= len(filtered_problems):
            click.echo("No problems on this page.")
            return

        filtered_problems = filtered_problems[skip:skip+limit]
        mock_data = {
            "data": {
                "problemsetQuestionList": {
                    "total": len(filtered_problems),
                    "questions": filtered_problems
                }
            }
        }

        problemset = parse_problemset_data(mock_data)

    else:
        cookie = get_cookie()
        csrf_token = extract_csrf_token(cookie)
        raw = fetch_problemset(cookie=cookie, csrf_token=csrf_token, tags=tag, difficulty=difficulty, limit=limit, skip=skip)

        if not raw:
            click.echo("Error: No data returned from server.")
            return

        problemset = parse_problemset_data(raw)

    formatter = ProblemSetFormatter(problemset)
    click.echo(formatter.get_formatted_questions())
