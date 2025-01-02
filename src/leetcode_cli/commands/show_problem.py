import click

from leetcode_cli.services.formatting_config_service import load_formatting_config
from leetcode_cli.formatters.problem_data_formatter import ProblemFormatter
from leetcode_cli.parsers.problem_parser import parse_problem_data
from leetcode_cli.data_fetchers.problem_data_fetcher import (
    fetch_problem_data,
    fetch_random_title_slug
)
from leetcode_cli.services.problemset_service import (
    filter_problems,
    load_problemset_metadata,
    get_problem_by_key_value,
    select_random_problem
)
from leetcode_cli.services.config_service import set_chosen_problem
from leetcode_cli.constants.problem_constants import POSSIBLE_TAGS
from leetcode_cli.services.theme_service import load_theme_data

def is_title_slug(value):
    return not value.isdigit()

@click.command(short_help='Show problem details')
@click.argument('title_slug_or_id', required=False)
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
@click.option(
    '--random', '-r',
    is_flag=True,
    help='Show a random problem'
)
@click.option(
    '--difficulty', '-d',
    type=click.Choice(["EASY", "MEDIUM", "HARD"], case_sensitive=False),
    metavar='DIFFICULTY',
    help='Filter random problems by difficulty (Requires --random).'
)
@click.option(
    '--tag', '-t',
    multiple=True,
    type=click.Choice(POSSIBLE_TAGS, case_sensitive=False),
    metavar='TAG_NAME',
    help='Filter random problems by tag (Requires --random).'
)
@click.option(
    '--use-downloaded', '-u',
    is_flag=True,
    help='Use downloaded problems metadata'
)
def show_cmd(title_slug_or_id, include, random, difficulty, tag, use_downloaded):
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

    if random:
        # Random problem approach
        if not use_downloaded:
            try:
                random_problem = fetch_random_title_slug(difficulty, tag)
                title_slug = random_problem["data"]["randomQuestion"].get("titleSlug", None)
                if not title_slug:
                    click.echo("No matching problems found.")
                    return
            except Exception as e:
                click.echo(f"Error fetching random problem: {e}")
                return
        else:
            problems_data = load_problemset_metadata()
            if not problems_data:
                click.echo("Error: Problems metadata not found. Use 'leetcode download-problems' first.")
                return
            filtered_problems = filter_problems(problems_data, difficulty, tag)
            if not filtered_problems:
                click.echo("No matching problems found.")
                return

            problem_data = select_random_problem(filtered_problems)
            title_slug = problem_data.get("titleSlug", None)

    else:
        # Direct slug/ID approach
        if difficulty or tag:
            click.echo("Error: --difficulty and --tag options only work with --random.")
            return

        if not title_slug_or_id:
            click.echo("Error: Need to specify a title slug or ID.")
            return

        if use_downloaded:
            problems_data = load_problemset_metadata()
            if not problems_data:
                click.echo("Error: Problems metadata not found. Use 'leetcode download-problems' first.")
                return

            if title_slug_or_id.isdigit():
                problem_data = get_problem_by_key_value(problems_data, "frontendQuestionId", title_slug_or_id)
            else:
                problem_data = get_problem_by_key_value(problems_data, "titleSlug", title_slug_or_id)

            title_slug = problem_data.get("titleSlug")
            if not title_slug:
                click.echo(f"Error: Problem with ID or slug '{title_slug_or_id}' not found.")
                return
        else:
            if is_title_slug(title_slug_or_id):
                title_slug = title_slug_or_id
            else:
                click.echo("Error: Showing by ID requires --use-downloaded.")
                return

    if not title_slug:
        click.echo("Error: Unable to determine the problem's title slug.")
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
