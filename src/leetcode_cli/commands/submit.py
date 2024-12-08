
# leetcode_cli/commands/submit.py
import click
from leetcode_cli.utils.user_utils import get_cookie, extract_csrf_token
from leetcode_cli.utils.code_utils import read_code_from_file, determine_language_from_extension
from leetcode_cli.data_fetching.submission_result_fetcher import fetch_submission_result
from leetcode_cli.parsers.submission_parser import parse_submission_result
from leetcode_cli.formatters.submission_formatter import SubmissionFormatter
from leetcode_cli.utils.user_utils import problem_data_from_path

@click.command(short_help='Submit a solution file')
@click.argument('file_path', required=True, type=click.Path(exists=True))
def submit_cmd(file_path):
    """Submit a solution file to LeetCode."""
    cookie = get_cookie()
    csrf_token = extract_csrf_token(cookie)
    if not cookie or not csrf_token:
        click.echo("Error: Missing authentication. Set cookie with 'leetcode config cookie <value>'")
        return

    # Extract title_slug from file path
    _, title_slug, file_extension = problem_data_from_path(file_path)
    code = read_code_from_file(file_path)
    language = determine_language_from_extension(file_extension)

    raw_submission = fetch_submission_result(cookie, csrf_token, title_slug, code, language)
    submission_res = parse_submission_result(raw_submission)
    formatter = SubmissionFormatter(submission_res)
    click.echo(formatter.get_formatted_submission())
