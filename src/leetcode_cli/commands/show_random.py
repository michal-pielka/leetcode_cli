import click
import logging

from leetcode_cli.constants.problem_constants import POSSIBLE_TAGS
from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.managers.problemset_manager import ProblemSetManager
from leetcode_cli.managers.formatting_config_manager import FormattingConfigManager
from leetcode_cli.managers.theme_manager import ThemeManager
from leetcode_cli.managers.problem_manager import ProblemManager
from leetcode_cli.managers.auth_service import AuthService
from leetcode_cli.formatters.problem_data_formatter import ProblemFormatter
from leetcode_cli.exceptions.exceptions import (
    ConfigError,
    FormattingError,
    ProblemError,
    ThemeError,
    ParsingError,
)

logger = logging.getLogger(__name__)


@click.command(short_help="Show a random problem")
@click.option(
    "--difficulty",
    "-d",
    type=click.Choice(["EASY", "MEDIUM", "HARD"], case_sensitive=False),
    metavar="DIFFICULTY",
    help="Filter random problems by difficulty.",
)
@click.option(
    "--tag",
    "-t",
    multiple=True,
    type=click.Choice(POSSIBLE_TAGS, case_sensitive=False),
    metavar="TAG_NAME",
    help="Filter random problems by tag.",
)
@click.option(
    "--include",
    "-i",
    multiple=True,
    type=click.Choice(
        ["title", "tags", "langs", "description", "examples", "constraints"],
        case_sensitive=False,
    ),
    metavar="SECTION",
    help="Sections to display. Overrides formatting_config.",
)
def random_cmd(difficulty, tag, include):
    """
    Show random problem details.

    By default, which sections are displayed depends on formatting_config.yaml
    ("problem_show" section). Use --include to override and show only specific sections.
    """
    try:
        config_manager = ConfigManager()
        auth_service = AuthService(config_manager)
        formatting_config_manager = FormattingConfigManager(config_manager)
        theme_manager = ThemeManager(config_manager)
        problemset_manager = ProblemSetManager(config_manager, auth_service)
        problem_manager = ProblemManager(
            config_manager, auth_service, problemset_manager
        )

        # Load format config
        formatting_config = formatting_config_manager.load_formatting_config()
        format_conf = formatting_config.problem_show

        # Override problem_show sections if user specified --include
        if include:
            for key in format_conf:
                format_conf[key] = False
            mapping = {
                "title": "show_title",
                "tags": "show_tags",
                "langs": "show_langs",
                "description": "show_description",
                "examples": "show_examples",
                "constraints": "show_constraints",
            }
            for item in include:
                if item in mapping:
                    format_conf[mapping[item]] = True

        # 1) Fetch random Problem object
        problem = problem_manager.get_random_problem(difficulty, tag)

        # 2) Update chosen problem in config
        # We'll need the slug. We added it to the object in get_random_problem
        slug = getattr(problem, "_title_slug", None)
        if not slug:
            # fallback if not present
            # (In your code, Problem does not store the slug natively.)
            # If we can't get slug, do nothing or raise an error
            click.echo("Error: Random problem has no slug. This shouldn't happen.")
            return

        config_manager.set_chosen_problem(slug)

        # 3) Format & display
        formatter = ProblemFormatter(problem, format_conf, theme_manager)
        formatted_str = formatter.get_formatted_problem()
        click.echo()
        click.echo(formatted_str)
        click.echo()

    except (ConfigError, ProblemError, ThemeError) as e:
        logger.error(e)
        click.echo(f"Error: {e}")

    except Exception as e:
        logger.exception("An unexpected error occurred in random_cmd.")
        click.echo(f"An error occurred: {e}")
