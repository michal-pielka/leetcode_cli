# leetcode_cli/commands/show_problem.py
import click
from leetcode_cli.utils.user_utils import load_problems_metadata, get_problem_by_key_value, set_chosen_problem, get_chosen_problem
from leetcode_cli.data_fetching.problem_fetcher import fetch_problem_data
from leetcode_cli.parsers.problem_parser import parse_problem_data
from leetcode_cli.formatters.problem_formatter import ProblemFormatter
from leetcode_cli.models.problem import Problem
import random

POSSIBLE_TAGS = [
    "array", "string", "hash-table", "dynamic-programming", "math", # ...
    # add all other tags as needed
]

def is_title_slug(value):
    return not value.isdigit()

@click.command(short_help='Show problem details')
@click.argument('title_slug_or_id', required=False)
@click.option('--include', multiple=True,
    type=click.Choice(["title", "tags", "langs", "description", "examples", "constraints"], case_sensitive=False),
    help='Sections to display. (default: all)')
@click.option('--random', is_flag=True, help='Show a random problem')
@click.option('--difficulty', type=click.Choice(["EASY", "MEDIUM", "HARD"], case_sensitive=False),
    help='Filter random problems by difficulty (Requires --random)')
@click.option('--tag', multiple=True, type=click.Choice(POSSIBLE_TAGS, case_sensitive=False),
    help='Filter random problems by tag (Requires --random)')
@click.option('--use-downloaded', is_flag=True, help='Use downloaded problems metadata')
def show_cmd(title_slug_or_id, include, random, difficulty, tag, use_downloaded):
    """Show problem details."""
    if random:
        if not use_downloaded:
            click.echo("Error: --random requires --use-downloaded.")
            return

        problems_data = load_problems_metadata()
        from leetcode_cli.utils.user_utils import filter_problems
        filtered_problems = filter_problems(problems_data, difficulty, tag)
        if not filtered_problems:
            click.echo("No matching problems found.")
            return
        problem_data = random.choice(filtered_problems)
        title_slug = problem_data.get("titleSlug")
    else:
        if difficulty or tag:
            click.echo("Error: --difficulty/--tag only work with --random.")
            return
        if not title_slug_or_id:
            click.echo("Error: Need a title_slug_or_id.")
            return

        if use_downloaded:
            problems_data = load_problems_metadata()
            if title_slug_or_id.isdigit():
                problem_data = get_problem_by_key_value(problems_data, "frontendQuestionId", title_slug_or_id)
            else:
                problem_data = get_problem_by_key_value(problems_data, "titleSlug", title_slug_or_id)
            title_slug = problem_data.get("titleSlug")
        else:
            # If not using downloaded, title_slug_or_id is assumed to be title_slug
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

    formatter = ProblemFormatter(problem)
    all_sections = {
        'title': formatter.title,
        'tags': formatter.tags,
        'langs': formatter.languages,
        'description': formatter.description,
        'examples': formatter.examples,
        'constraints': formatter.constraints
    }

    if not include:
        sections = all_sections.keys()
    else:
        sections = include

    click.echo()
    for sec in sections:
        content = all_sections.get(sec)
        if content:
            val = content()
            if val:
                click.echo(val)
                click.echo()
