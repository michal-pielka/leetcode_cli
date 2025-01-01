import click

from leetcode_cli.services.config_service import get_cookie, extract_csrf_token
from leetcode_cli.services.download_service import load_problems_metadata, filter_problems
from leetcode_cli.data_fetching.problemset_fetcher import fetch_problemset
from leetcode_cli.parsers.problemset_data_parser import parse_problemset_data
from leetcode_cli.formatters.problemset_formatter import ProblemSetFormatter
from leetcode_cli.constants.problem_constants import POSSIBLE_TAGS
from leetcode_cli.services.theme_service import load_theme_data

def validate_positive_integer(ctx, param, value):
    if value <= 0:
        raise click.BadParameter('Must be greater than 0.')
    return value

@click.command(short_help='List LeetCode problems with optional filters')
@click.option(
    '--difficulty', '-d',
    type=click.Choice(["EASY", "MEDIUM", "HARD"], case_sensitive=False),
    metavar='DIFFICULTY',
    help='Filter by difficulty (default: all difficulties).'
)
@click.option(
    '--tag', '-t',
    multiple=True,
    type=click.Choice(POSSIBLE_TAGS, case_sensitive=False),
    metavar='TAG_NAME',
    help='Filter by tag (default: all tags).'
)
@click.option(
    '--limit', '-l',
    type=int,
    default=50,
    callback=validate_positive_integer,
    metavar='LIMIT',
    help='Number of results per page (default: 50).'
)
@click.option(
    '--page', '-p',
    type=int,
    default=1,
    callback=validate_positive_integer,
    metavar='PAGE',
    help='Page number to display (default: 1).'
)
@click.option(
    '--use-downloaded', '-u',
    is_flag=True,
    help='Use downloaded problems metadata.'
)
def list_cmd(difficulty, tag, limit, page, use_downloaded):
    """
    List LeetCode problems with optional filters.
    """
    skip = (page - 1) * limit

    if use_downloaded:
        problems_data = load_problems_metadata()
        if not problems_data:
            click.echo("Error: No local metadata found. Use 'leetcode download_problems' first.")
            return

        filtered_problems = filter_problems(problems_data, difficulty, tag)
        if not filtered_problems:
            click.echo("No problems found with the specified filters.")
            return

        if skip >= len(filtered_problems):
            click.echo("No problems found on this page.")
            return

        paginated_problems = filtered_problems[skip:skip+limit]
        mock_data = {
            "data": {
                "problemsetQuestionList": {
                    "total": len(filtered_problems),
                    "questions": paginated_problems
                }
            }
        }

        problemset = parse_problemset_data(mock_data)

    else:
        cookie = get_cookie()
        csrf_token = extract_csrf_token(cookie)

        try:
            raw = fetch_problemset(
                cookie=cookie,
                csrf_token=csrf_token,
                tags=tag if tag else None,
                difficulty=difficulty if difficulty else None,
                limit=limit,
                skip=skip
            )

        except Exception as e:
            click.echo(f"Error fetching problem set: {e}")
            return

        problemset = parse_problemset_data(raw)

    theme_data = load_theme_data()
    formatter = ProblemSetFormatter(problemset, theme_data)
    click.echo(formatter.get_formatted_questions())
