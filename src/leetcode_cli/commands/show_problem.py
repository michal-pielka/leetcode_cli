import click

from leetcode_cli.graphics.ansi_codes import ANSI_RESET, ANSI_CODES

from leetcode_cli.services import problemset_service
from leetcode_cli.services.config_service import set_chosen_problem
from leetcode_cli.services.theme_service import load_theme_data
from leetcode_cli.services.formatting_config_service import load_formatting_config
from leetcode_cli.services.problemset_service import load_problemset_metadata, get_title_slug

from leetcode_cli.formatters.problem_data_formatter import ProblemFormatter

from leetcode_cli.parsers.problem_data_parser import parse_problem_data

from leetcode_cli.data_fetchers.problem_data_fetcher import fetch_problem_data

def is_id(value):
    return value.isdigit()

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

    user_config = load_formatting_config()
    format_conf = user_config.problem_show
    theme_data = load_theme_data()

    # Override format_conf if --include is used
    if include:
        for key in format_conf.keys():
            format_conf[key] = False

        for item in include:
            if item == "title":
                format_conf["show_title"] = True
            elif item == "tags":
                format_conf["show_tags"] = True
            elif item == "langs":
                format_conf["show_langs"] = True
            elif item == "description":
                format_conf["show_description"] = True
            elif item == "examples":
                format_conf["show_examples"] = True
            elif item == "constraints":
                format_conf["show_constraints"] = True

    if is_id(title_slug_or_id):
        problemset_metadata = load_problemset_metadata()
        if not problemset_metadata:
            click.echo(f"In order to show problems by ID you need to download problems metadata using {ANSI_CODES['ITALIC']}leetcode download-problems{ANSI_RESET}.")
            return

        title_slug = get_title_slug(problemset_metadata, title_slug_or_id)

    else:
        title_slug = title_slug_or_id

    if not title_slug:
        click.echo("Error: Problem with this title slug or ID can't be found.")
        return

    try:
        raw_data = fetch_problem_data(title_slug)
        if (
            not raw_data
            or 'data' not in raw_data
            or 'question' not in raw_data['data']
            or not raw_data['data']['question']
        ):
            click.echo("Error: Could not fetch problem data.")
            return

        problem = parse_problem_data(raw_data)
        set_chosen_problem(title_slug)

        formatter = ProblemFormatter(problem, format_conf, theme_data)
        formatted_str = formatter.get_formatted_problem()

        click.echo()
        click.echo(formatted_str)
        click.echo()

    except Exception as e:
        click.echo(f"An error occurred: {e}")
