import click

from leetcode_cli.constants.problem_constants import POSSIBLE_TAGS
from leetcode_cli.services.formatting_config_service import load_formatting_config
from leetcode_cli.services.theme_service import load_theme_data
from leetcode_cli.services.config_service import set_chosen_problem

from leetcode_cli.formatters.problem_data_formatter import ProblemFormatter
from leetcode_cli.formatters.problem_data_formatter import ProblemFormatter

from leetcode_cli.data_fetchers.problem_data_fetcher import fetch_random_title_slug, fetch_problem_data

from leetcode_cli.parsers.problem_data_parser import parse_problem_data

@click.command(short_help='Show a random problem')
@click.option(
    '--difficulty', '-d',
    type=click.Choice(["EASY", "MEDIUM", "HARD"], case_sensitive=False),
    metavar='DIFFICULTY',
    help='Filter random problems by difficulty.'
)
@click.option(
    '--tag', '-t',
    multiple=True,
    type=click.Choice(POSSIBLE_TAGS, case_sensitive=False),
    metavar='TAG_NAME',
    help='Filter random problems by tag.'
)
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
def random_cmd(difficulty, tag, include):
    """
    Show a random LeetCode problem with optional filters.
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
    try:
        random_problem = fetch_random_title_slug(difficulty, tag)
        title_slug = random_problem["data"]["randomQuestion"].get("titleSlug", None)
        if not title_slug:
            click.echo("No matching problems found.")
            return

    except Exception as e:
        click.echo(f"Error fetching random problem: {e}")
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
