import click
import logging

from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.managers.code_manager import CodeManager
from leetcode_cli.managers.problemset_manager import ProblemSetManager
from leetcode_cli.managers.formatting_config_manager import FormattingConfigManager
from leetcode_cli.managers.theme_manager import ThemeManager
from leetcode_cli.managers.problem_manager import ProblemManager

from leetcode_cli.data_fetchers.problem_data_fetcher import fetch_problem_testcases
from leetcode_cli.data_fetchers.interpretation_result_fetcher import fetch_interpretation_result
from leetcode_cli.parsers.interpretation_result_parser import parse_interpretation_result
from leetcode_cli.formatters.interpretation_result_formatter import InterpretationFormatter

from leetcode_cli.exceptions.exceptions import ConfigError, CodeError, ProblemError

logger = logging.getLogger(__name__)

@click.command(short_help='Test a solution file')
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
    """
    Test a solution file with example testcases.
    """
    try:
        # 1) Initialize managers
        config_manager = ConfigManager()
        code_manager = CodeManager(config_manager)
        problem_manager = ProblemManager(config_manager)
        formatting_config_manager = FormattingConfigManager(config_manager)
        theme_manager = ThemeManager(config_manager)
        problemset_manager = ProblemSetManager(config_manager)

        # 2) Load formatting config
        formatting_config = formatting_config_manager.load_formatting_config()
        format_conf = formatting_config.interpretation

        # If user passed --include flags, override
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

        # 3) Retrieve cookie & CSRF from config
        cookie = config_manager.get_cookie()
        csrf_token = config_manager.extract_csrf_token()
        if not cookie or not csrf_token:
            click.echo("Error: Missing authentication tokens.")
            return

        # 4) Parse the local file path => (question_id, title_slug, file_extension)
        _, title_slug, file_extension = problemset_manager.problem_data_from_path(file_path)
        question_id = problem_manager.get_problem_id(title_slug)

        # 5) Read code from local file
        code = code_manager.read_code_from_file(file_path)

        # 6) Determine language from extension
        lang_slug = code_manager.determine_language_from_extension(file_extension)

        # 7) Fetch testcases from LeetCode
        testcases_data = fetch_problem_testcases(title_slug)
        if (
            not testcases_data
            or "data" not in testcases_data
            or "question" not in testcases_data["data"]
            or "exampleTestcases" not in testcases_data["data"]["question"]
        ):
            click.echo(f"Error: Unable to fetch testcases for '{title_slug}'.")
            return

        problem_testcases = testcases_data['data']['question']['exampleTestcases']

        # 8) Run interpretation
        raw_interpretation = fetch_interpretation_result(
            cookie, csrf_token, title_slug, code, lang_slug, problem_testcases, int(question_id)
        )
        interpretation_res = parse_interpretation_result(raw_interpretation)

        # 9) Format result (InterpretationFormatter with multiline `_format_field`)
        # We pass testcases as a list of dicts, minimal example:
        # e.g. [{"input": problem_testcases.split("\n")}]
        # If you had multiple testcases, you might parse them differently.

        formatter = InterpretationFormatter(
            interpretation_res,
            problem_testcases,
            format_conf,
            theme_manager
        )
        formatted_str = formatter.get_formatted_interpretation()

        # 10) Display
        click.echo(formatted_str)

    except (ConfigError, CodeError, ProblemError) as e:
        logger.error(e)
        click.echo(f"Error: {e}")
    except Exception as e:
        logger.exception("An unexpected error occurred during test_cmd.")
        click.echo("An unexpected error occurred. Please try again.", err=True)
