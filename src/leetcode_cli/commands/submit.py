import click
import logging

from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.managers.formatting_config_manager import FormattingConfigManager, ConfigError
from leetcode_cli.managers.code_manager import CodeManager, CodeError
from leetcode_cli.managers.theme_manager import ThemeManager, ThemeError
from leetcode_cli.managers.problem_manager import ProblemManager, ProblemError
from leetcode_cli.managers.problemset_manager import ProblemSetManager

from leetcode_cli.data_fetchers.submission_result_fetcher import fetch_submission_result
from leetcode_cli.parsers.submission_result_parser import parse_submission_result
from leetcode_cli.formatters.submission_result_formatter import SubmissionFormatter

logger = logging.getLogger(__name__)

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
    try:
        # 1) Initialize managers
        config_manager = ConfigManager()
        formatting_config_manager = FormattingConfigManager(config_manager)
        code_manager = CodeManager(config_manager)
        theme_manager = ThemeManager(config_manager)
        problem_manager = ProblemManager(config_manager)
        problemset_manager = ProblemSetManager(config_manager)

        # 2) Load formatting config
        formatting_config = formatting_config_manager.load_formatting_config()
        format_conf = formatting_config.submission

        # If user passed --include, override
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

        # 3) Authentication
        cookie = config_manager.get_cookie()
        csrf_token = config_manager.extract_csrf_token()
        if not cookie or not csrf_token:
            click.echo("Error: Missing authentication. Set cookie with 'leetcode config cookie <value>'")
            return

        # 4) Parse local file path => (question_id, title_slug, file_extension)
        try:
            _, title_slug, file_extension = problemset_manager.problem_data_from_path(file_path)
            question_id = problem_manager.get_problem_id(title_slug)
        except ProblemError as e:
            click.echo(f"Error: {e}")
            return

        # 5) Read code from local file
        try:
            code = code_manager.read_code_from_file(file_path)
        except CodeError as e:
            click.echo(f"Error: {e}")
            return

        # 6) Determine language from extension
        try:
            lang_slug = code_manager.determine_language_from_extension(file_extension)
        except CodeError as e:
            click.echo(f"Error: {e}")
            return

        # 7) Fetch submission result from LeetCode
        try:
            raw_submission = fetch_submission_result(
                cookie, csrf_token, title_slug, code, lang_slug, int(question_id)
            )
            submission_res = parse_submission_result(raw_submission)
        except Exception as e:
            logger.error(f"Failed to fetch or parse submission result: {e}")
            click.echo(f"Error: {e}")
            return

        # 8) Format and display submission result
        try:
            formatter = SubmissionFormatter(submission_res, format_conf, theme_manager)
            formatted_str = formatter.get_formatted_submission()
            click.echo(formatted_str)
        except Exception as e:
            logger.error(f"Failed to format submission result: {e}")
            click.echo(f"Error: {e}")

    except (ConfigError, ThemeError) as e:
        logger.error(e)
        click.echo(f"Configuration/Theme Error: {e}", err=True)
    except Exception as e:
        logger.exception("An unexpected error occurred during submission.")
        click.echo("An unexpected error occurred. Please try again.", err=True)
