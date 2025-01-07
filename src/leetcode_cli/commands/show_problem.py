import click
import logging

from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.managers.problem_manager import ProblemManager
from leetcode_cli.managers.formatting_config_manager import FormattingConfigManager
from leetcode_cli.managers.theme_manager import ThemeManager
from leetcode_cli.formatters.problem_data_formatter import ProblemFormatter
from leetcode_cli.exceptions.exceptions import ConfigError, ProblemError, ThemeError, ProblemError

logger = logging.getLogger(__name__)

@click.command(short_help='Show problem details')
@click.argument('title_slug_or_id', required=True)
@click.option(
    '--include', '-i',
    multiple=True,
    type=click.Choice(
        ["title", "tags", "langs", "description", "examples", "constraints"], 
        case_sensitive=False
    ),
    metavar='SECTION',
    help='Sections to display. Overrides formatting_config.'
)
def show_cmd(title_slug_or_id, include):
    """
    Show problem details.

    By default, which sections are displayed depends on formatting_config.yaml
    ("problem_show" section). Use --include to override and show only specific sections.
    """
    try:
        # Initialize managers
        config_manager = ConfigManager()
        formatting_config_manager = FormattingConfigManager(config_manager)
        formatting_config = formatting_config_manager.load_formatting_config()
        problem_manager = ProblemManager(config_manager)
        theme_manager = ThemeManager(config_manager)
        
        # Override formatting configuration if --include is used
        format_conf = formatting_config.problem_show
        if include:
            for key in format_conf.keys():
                format_conf[key] = False

            mapping = {
                "title": "show_title",
                "tags": "show_tags",
                "langs": "show_langs",
                "description": "show_description",
                "examples": "show_examples",
                "constraints": "show_constraints"
            }
            for item in include:
                key = mapping.get(item.lower())
                if key:
                    format_conf[key] = True

        # Fetch problem data
        try:
            problem = problem_manager.get_specific_problem(title_slug_or_id)

        except ProblemError as e:
            click.echo(f"Error: {e}")
            return

        if title_slug_or_id.isdigit():
            # we used that as frontend ID, so fetch the real slug
            slug = problem_manager.get_title_slug_for_id(title_slug_or_id)
        else:
            # else it's a slug
            slug = title_slug_or_id
        
        config_manager.set_chosen_problem(slug)
        # Format and display problem
        try:
            # Pass the theme_manager (not theme_data)
            formatter = ProblemFormatter(problem, format_conf, theme_manager)
            formatted_str = formatter.get_formatted_problem()
            click.echo()
            click.echo(formatted_str)
            click.echo()

        except Exception as e:
            logger.error(f"Failed to format problem data: {e}")
            click.echo(f"Error: {e}")

    except (ConfigError, ThemeError) as e:
        logger.error(e)
        click.echo(f"Configuration/Theme Error: {e}", err=True)

    except Exception as e:
        logger.exception("An unexpected error occurred while showing the problem.")
        click.echo("An unexpected error occurred. Please try again.", err=True)
