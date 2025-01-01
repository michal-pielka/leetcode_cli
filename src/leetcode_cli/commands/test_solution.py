import click

from leetcode_cli.services.config_service import get_cookie, extract_csrf_token
from leetcode_cli.services.code_service import read_code_from_file, determine_language_from_extension
from leetcode_cli.services.download_service import problem_data_from_path
from leetcode_cli.data_fetching.problem_fetcher import fetch_problem_testcases
from leetcode_cli.data_fetching.interpretation_result_fetcher import fetch_interpretation_result
from leetcode_cli.parsers.interpretation_parser import parse_interpretation_result
from leetcode_cli.formatters.interpretation_formatter import InterpretationFormatter
from leetcode_cli.services.formatting_service import load_formatting_config
from leetcode_cli.services.theme_service import load_theme_data

@click.command(short_help='Test a solution files')
@click.argument('file_path', required=True, type=click.Path(exists=True), metavar='FILE_PATH')
@click.option(
    '--include', '-i',
    multiple=True,
    type=click.Choice(
        [
            "language",
            "testcases",
            "expected_output",
            "code_output",
            "stdout",
            "error_messages",
            "detailed_error_messages",
        ],
        case_sensitive=False
    ),
    metavar='SECTION',
    help='Sections to display. Overrides formatting_config.'
)
def test_cmd(file_path, include):
    """Test a solution file with example testcases."""
    
    user_config = load_formatting_config()
    format_conf = user_config.interpretation
    theme_data = load_theme_data()

    if include:
        for key in format_conf.keys():
            format_conf[key] = False

        for item in include:
            if item == "language":
                format_conf["show_language"] = True
            elif item == "testcases":
                format_conf["show_testcases"] = True
            elif item == "expected_output":
                format_conf["show_expected_output"] = True
            elif item == "code_output":
                format_conf["show_code_output"] = True
            elif item == "stdout":
                format_conf["show_stdout"] = True
            elif item == "error_messages":
                format_conf["show_error_messages"] = True
            elif item == "detailed_error_messages":
                format_conf["show_detailed_error_messages"] = True

    cookie = get_cookie()
    csrf_token = extract_csrf_token(cookie)
    if not cookie or not csrf_token:
        click.echo("Error: Missing authentication tokens.")
        return

    _, title_slug, file_extension = problem_data_from_path(file_path)
    code = read_code_from_file(file_path)
    language = determine_language_from_extension(file_extension)

    testcases_data = fetch_problem_testcases(title_slug)
    problem_testcases = testcases_data['data']['question']['exampleTestcases']

    raw_interpretation = fetch_interpretation_result(
        cookie, csrf_token, title_slug, code, language, problem_testcases
    )
    interpretation_res = parse_interpretation_result(raw_interpretation)

    formatter = InterpretationFormatter(interpretation_res, problem_testcases, format_conf, theme_data)
    formatted_str = formatter.get_formatted_interpretation()

    click.echo(formatted_str)
