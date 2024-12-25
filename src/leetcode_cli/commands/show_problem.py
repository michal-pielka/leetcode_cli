import click

from leetcode_cli.utils.formatting_config_utils import load_formatting_config
from leetcode_cli.formatters.problem_formatter import ProblemFormatter
from leetcode_cli.parsers.problem_parser import parse_problem_data
from leetcode_cli.data_fetching.problem_fetcher import (
    fetch_problem_data,
    fetch_random_title_slug
)
from leetcode_cli.utils.download_problems_utils import (
    filter_problems,
    load_problems_metadata,
    get_problem_by_key_value,
    select_random_problem
)
from leetcode_cli.utils.config_utils import set_chosen_problem
from leetcode_cli.constants.problem_constants import POSSIBLE_TAGS

def is_title_slug(value):
    return not value.isdigit()

@click.command(short_help='Show problem details')
@click.argument('title_slug_or_id', required=False)
@click.option('--include', multiple=True,
    type=click.Choice(
        ["title", "tags", "langs", "description", "examples", "constraints"], 
        case_sensitive=False
    ),
    help='Sections to display. Overrides formatting_config.'
)
@click.option('--random', is_flag=True, help='Show a random problem')
@click.option('--difficulty', type=click.Choice(["EASY", "MEDIUM", "HARD"], case_sensitive=False),
              help='Filter random problems by difficulty (Requires --random).')
@click.option('--tag', multiple=True, type=click.Choice(POSSIBLE_TAGS, case_sensitive=False),
              help='Filter random problems by tag (Requires --random).')
@click.option('--use-downloaded', is_flag=True, help='Use downloaded problems metadata')
def show_cmd(title_slug_or_id, include, random, difficulty, tag, use_downloaded):
    """
    Show problem details.

    By default, which sections are displayed depends on formatting_config.json ("problem_show" section).
    Use --include to override and show only specific sections.
    """

    user_config = load_formatting_config()
    format_conf = user_config["problem_show"]

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
        if not use_downloaded:
            random_problem = fetch_random_title_slug(difficulty, tag)
            if not random_problem.get("data", {}).get("randomQuestion"):
                click.echo("No matching problems found.")
                return
            title_slug = random_problem["data"]["randomQuestion"].get("titleSlug", None)
        else:
            problems_data = load_problems_metadata()
            if not problems_data:
                click.echo("Error: problems' metadata not found, use leetcode download-problems.")
                return
            filtered_problems = filter_problems(problems_data, difficulty, tag)
            if not filtered_problems:
                click.echo("No matching problems found.")
                return
            problem_data = select_random_problem(filtered_problems)
            title_slug = problem_data.get("titleSlug", None)

    else:
        if difficulty or tag:
            click.echo("Error: --difficulty/--tag only work with --random.")
            return

        if not title_slug_or_id:
            click.echo("Error: Need title slug or id.")
            return

        if use_downloaded:
            problems_data = load_problems_metadata()
            if not problems_data:
                click.echo("Error: problems' metadata not found, use leetcode download-problems.")
                return
            if title_slug_or_id.isdigit():
                problem_data = get_problem_by_key_value(problems_data, "frontendQuestionId", title_slug_or_id)
            else:
                problem_data = get_problem_by_key_value(problems_data, "titleSlug", title_slug_or_id)
            title_slug = problem_data.get("titleSlug")

        else:
            if is_title_slug(title_slug_or_id):
                title_slug = title_slug_or_id
            else:
                click.echo("Error: Show by ID requires --use-downloaded.")
                return

    if not title_slug:
        click.echo("Error: Unable to determine title_slug.")
        return

    raw_data = fetch_problem_data(title_slug)
    if not raw_data or 'data' not in raw_data or 'question' not in raw_data['data'] or not raw_data['data']['question']:
        click.echo("Error: Could not fetch problem data.")
        return

    problem = parse_problem_data(raw_data)

    set_chosen_problem(title_slug)

    formatter = ProblemFormatter(problem, format_conf)
    formatted_str = formatter.get_formatted_problem()

    click.echo(formatted_str)
