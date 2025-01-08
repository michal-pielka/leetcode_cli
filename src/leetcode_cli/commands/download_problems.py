import click
import logging

from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.managers.auth_service import AuthService
from leetcode_cli.managers.problemset_manager import ProblemSetManager
from leetcode_cli.data_fetchers.problemset_data_fetcher import fetch_problemset_metadata
from leetcode_cli.exceptions.exceptions import ProblemSetError, ConfigError

logger = logging.getLogger(__name__)


@click.command(short_help="Download all problems metadata")
def download_problems_cmd():
    """
    Download all LeetCode problems metadata and save locally in order to speed up some commands and enable showing/creating by ID
    """
    try:
        # Initialize managers
        config_manager = ConfigManager()
        auth_service = AuthService(config_manager)
        problemset_manager = ProblemSetManager(config_manager, auth_service)

        # Fetch problemset metadata
        try:
            problems_data = fetch_problemset_metadata()
            if not problems_data:
                click.echo("Error: Failed to fetch problems metadata.")
                return

        except Exception as e:
            logger.error(f"Failed to fetch problemset metadata: {e}")
            click.echo(f"Error: Failed to fetch problems metadata. {e}")
            return

        # Save problemset metadata
        try:
            problemset_manager.save_problemset_metadata(problems_data)
            problems_path = problemset_manager.get_problems_data_path()
            click.echo(f"Problems metadata downloaded to '{problems_path}'.")

        except ProblemSetError as e:
            click.echo(f"Error: {e}")
            return

    except ConfigError as e:
        logger.error(e)
        click.echo(f"Configuration Error: {e}", err=True)

    except Exception as e:
        logger.exception(
            "An unexpected error occurred during problems metadata download."
        )
        click.echo("An unexpected error occurred. Please try again.", err=True)
