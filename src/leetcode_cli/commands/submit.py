# file: commands/submit.py

import click
import logging

from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.managers.auth_service import AuthService
from leetcode_cli.managers.formatting_config_manager import FormattingConfigManager
from leetcode_cli.managers.code_manager import CodeManager
from leetcode_cli.managers.theme_manager import ThemeManager
from leetcode_cli.managers.problem_manager import ProblemManager
from leetcode_cli.managers.problemset_manager import ProblemSetManager

from leetcode_cli.formatters.submission_result_formatter import SubmissionFormatter
from leetcode_cli.exceptions.exceptions import ConfigError, CodeError, ProblemError, ThemeError

logger = logging.getLogger(__name__)

@click.command(short_help='Submit a solution file to LeetCode')
@click.argument('file_path', required=True, type=click.Path(exists=True))
@click.option(
    '--include', '-i',
    multiple=True,
    type=click.Choice([
        "language",
        "testcases",
        "runtime_memory",
        "code_output",
        "stdout",
        "error_messages",
        "detailed_error_messages",
        "expected_output",
    ], case_sensitive=False),
    metavar='SECTION',
    help='Sections to display. Overrides formatting_config.'
)
def submit_cmd(file_path, include):
    """
    Submit a solution file to LeetCode.
    """
    try:
        config_manager = ConfigManager()
        auth_service = AuthService(config_manager)
        formatting_config_manager = FormattingConfigManager(config_manager)
        code_manager = CodeManager(config_manager)
        theme_manager = ThemeManager(config_manager)
        problemset_manager = ProblemSetManager(config_manager, auth_service)
        problem_manager = ProblemManager(config_manager, auth_service, problemset_manager)

        # Load formatting config
        formatting_config = formatting_config_manager.load_formatting_config()
        format_conf = formatting_config.submission

        # override if user passed --include
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

        # Parse path => (id, slug, ext)
        _, title_slug, file_extension = problem_manager.problem_data_from_path(file_path)

        # read code
        code = code_manager.read_code_from_file(file_path)

        # lang
        lang_slug = code_manager.determine_language_from_extension(file_extension)

        # manager fetches + parses the submission result
        submission_res = problem_manager.get_submission_result(
            title_slug=title_slug,
            code=code,
            lang_slug=lang_slug
        )

        # format
        formatter = SubmissionFormatter(submission_res, format_conf, theme_manager)
        result_str = formatter.get_formatted_submission()
        click.echo(result_str)

    except (ConfigError, ThemeError, CodeError, ProblemError) as e:
        logger.error(e)
        click.echo(f"Error: {e}")

    except Exception as e:
        logger.exception("Unexpected error in submit_cmd.")
        click.echo("An unexpected error occurred.", err=True)
