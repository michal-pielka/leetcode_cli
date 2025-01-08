import click
import logging

from leetcode_cli.constants.problem_constants import POSSIBLE_TAGS
from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.managers.theme_manager import ThemeManager
from leetcode_cli.managers.problemset_manager import ProblemSetManager
from leetcode_cli.managers.auth_service import AuthService
from leetcode_cli.formatters.problemset_data_formatter import ProblemSetFormatter
from leetcode_cli.exceptions.exceptions import ProblemSetError, ThemeError, ConfigError

logger = logging.getLogger(__name__)

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
    callback=lambda ctx, param, value: value if value > 0 else click.BadParameter('Must be greater than 0.'),
    metavar='LIMIT',
    help='Number of results per page (default: 50).'
)
@click.option(
    '--page', '-p',
    type=int,
    default=1,
    callback=lambda ctx, param, value: value if value > 0 else click.BadParameter('Must be greater than 0.'),
    metavar='PAGE',
    help='Page number to display (default: 1).'
)
def list_cmd(difficulty, tag, limit, page):
    """
    List LeetCode problems with optional filters.
    """
    try:
        # Initialize managers
        config_manager = ConfigManager()
        auth_service = AuthService(config_manager)
        problemset_manager = ProblemSetManager(config_manager, auth_service)
        theme_manager = ThemeManager(config_manager)


        # Get problemset data
        try:
            problemset = problemset_manager.get_problemset(
                tags=tag,
                difficulty=difficulty,
                limit=limit,
                page=page
            )

        except Exception as e:
            click.echo(f"Error: {e}")
            return

        # Format and display problemset
        try:
            # Pass the ThemeManager instead of the raw theme_data
            formatter = ProblemSetFormatter(problemset, theme_manager)
            click.echo()
            click.echo(formatter.get_formatted_questions())
            click.echo()

        except Exception as e:
            logger.error(f"Failed to format problem set: {e}")
            click.echo(f"Error: {e}")

    except (ConfigError, ThemeError, ProblemSetError) as e:
        logger.error(e)
        click.echo(f"Error: {e}", err=True)

    except Exception as e:
        logger.exception("An unexpected error occurred while listing problems.")
        click.echo("An unexpected error occurred. Please try again.", err=True)
