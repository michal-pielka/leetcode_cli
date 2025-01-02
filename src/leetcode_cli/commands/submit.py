import click

from leetcode_cli.services.config_service import get_cookie, extract_csrf_token
from leetcode_cli.services.problemset_service import problem_data_from_path
from leetcode_cli.services.code_service import read_code_from_file, determine_language_from_extension
from leetcode_cli.data_fetchers.submission_result_fetcher import fetch_submission_result
from leetcode_cli.parsers.submission_parser import parse_submission_result
from leetcode_cli.formatters.submission_result_formatter import SubmissionFormatter
from leetcode_cli.services.formatting_config_service import load_formatting_config
from leetcode_cli.services.theme_service import load_theme_data

@click.command(short_help='Submit a solution file to LeetCode')
@click.argument('file_path', required=True, type=click.Path(exists=True), metavar='FILE_PATH')
@click.option(
    '--include', '-i',
    multiple=True,
    type=click.Choice(
        [
            "language",
            "testcases",
            "runtime_memory",
            "code_output",
            "stdout",
            "error_messages",
            "detailed_error_messages",
            "expected_output",
        ],
        case_sensitive=False
    ),
    metavar='SECTION',
    help='Sections to display. Overrides formatting_config.'
)
def submit_cmd(file_path, include):
    """
    Submit a solution file to LeetCode.
    """
    user_config = load_formatting_config()
    format_conf = user_config.submission
    theme_data = load_theme_data()
    
    if include:
        for key in format_conf.keys():
            format_conf[key] = False
        
        for item in include:
            if item == "language":
                format_conf["show_language"] = True
            elif item == "testcases":
                format_conf["show_testcases"] = True
            elif item == "runtime_memory":
                format_conf["show_runtime_memory"] = True
            elif item == "code_output":
                format_conf["show_code_output"] = True
            elif item == "stdout":
                format_conf["show_stdout"] = True
            elif item == "error_messages":
                format_conf["show_error_messages"] = True
            elif item == "detailed_error_messages":
                format_conf["show_detailed_error_messages"] = True
            elif item == "expected_output":
                format_conf["show_expected_output"] = True

    cookie = get_cookie()
    csrf_token = extract_csrf_token(cookie)
    if not cookie or not csrf_token:
        click.echo("Error: Missing authentication. Set cookie with 'leetcode config cookie <value>'")
        return

    _, title_slug, file_extension = problem_data_from_path(file_path)
    code = read_code_from_file(file_path)
    language = determine_language_from_extension(file_extension)

    raw_submission = fetch_submission_result(cookie, csrf_token, title_slug, code, language)
    submission_res = parse_submission_result(raw_submission)

    formatter = SubmissionFormatter(submission_res, format_conf, theme_data)
    formatted_str = formatter.get_formatted_submission()

    click.echo(formatted_str)
