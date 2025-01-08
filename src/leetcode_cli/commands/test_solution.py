import click
import logging

from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.managers.auth_service import AuthService
from leetcode_cli.managers.code_manager import CodeManager
from leetcode_cli.managers.problem_manager import ProblemManager
from leetcode_cli.managers.formatting_config_manager import FormattingConfigManager
from leetcode_cli.managers.theme_manager import ThemeManager
from leetcode_cli.managers.problemset_manager import ProblemSetManager

from leetcode_cli.formatters.interpretation_result_formatter import InterpretationFormatter
from leetcode_cli.exceptions.exceptions import ConfigError, CodeError, ProblemError, ThemeError

logger = logging.getLogger(__name__)

@click.command(short_help='Test a solution file')
@click.argument('file_path', required=True, type=click.Path(exists=True))
@click.option(
    '--include', '-i',
    multiple=True,
    type=click.Choice([
        "language",
        "testcases",
        "expected_output",
        "code_output",
        "stdout",
        "error_messages",
        "detailed_error_messages",
    ], case_sensitive=False),
    metavar='SECTION',
    help='Sections to display. Overrides formatting_config.'
)
def test_cmd(file_path, include):
    """
    Test a solution file with example testcases.
    """
    try:
        # 1) Setup
        config_manager = ConfigManager()
        auth_service = AuthService(config_manager)
        code_manager = CodeManager(config_manager)
        problemset_manager = ProblemSetManager(config_manager, auth_service)
        problem_manager = ProblemManager(config_manager, auth_service, problemset_manager)
        formatting_config_manager = FormattingConfigManager(config_manager)
        theme_manager = ThemeManager(config_manager)

        # 2) Load format config
        formatting_config = formatting_config_manager.load_formatting_config()
        format_conf = formatting_config.interpretation

        # 3) Override formatting sections if needed
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

        # 4) Parse local file => question_id, slug, extension
        _, title_slug, file_extension = problem_manager.problem_data_from_path(file_path)

        # 5) Read code
        code = code_manager.read_code_from_file(file_path)

        # 6) Determine lang
        lang_slug = code_manager.determine_language_from_extension(file_extension)

        # 7) Get example testcases from the manager (optional approach)
        testcases_str = problem_manager.get_example_testcases(title_slug)

        # 8) Retrieve interpretation result from manager
        interpretation_res = problem_manager.get_interpretation_result(
            title_slug=title_slug,
            code=code,
            lang_slug=lang_slug,
            testcases=testcases_str
        )

        # 9) Format
        formatter = InterpretationFormatter(
            interpretation_res,
            testcases_str,  # pass as a single string
            format_conf,
            theme_manager
        )
        output_str = formatter.get_formatted_interpretation()

        # 10) Print
        click.echo(output_str)

    except (ConfigError, CodeError, ProblemError, ThemeError) as e:
        logger.error(e)
        click.echo(f"Error: {e}")

    except Exception as e:
        logger.exception("Unexpected error in test_cmd.")
        click.echo("An unexpected error occurred.", err=True)
