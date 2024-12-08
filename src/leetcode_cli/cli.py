import click


from leetcode_cli.data_fetching.problem_fetcher import fetch_problem_data
from leetcode_cli.parsersNEW.problem_parser import parse_problem_data
from leetcode_cli.formatters.problem_formatter import ProblemFormatter
from leetcode_cli.data_fetching.problemset_fetcher import fetch_problemset

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'], max_content_width=200)

@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """LeetCode CLI Tool

    Manage your LeetCode activities directly from the command line.
    """
    if ctx.invoked_subcommand is None:
        click.echo("testHELP")


@cli.command(short_help='Configure user settings')
def test_list():
    from leetcode_cli.data_fetching.problemset_fetcher import fetch_problemset
    from leetcode_cli.parsersNEW.problemset_data_parser import parse_problemset_data
    from leetcode_cli.formatters.problemset_formatter import ProblemSetFormatter
        
    problemset_raw = fetch_problemset(None, None, None, None, None, None)
    parsed = parse_problemset_data(problemset_raw)
    formatted_problemset = ProblemSetFormatter(parsed)
    print(formatted_problemset.get_formatted_questions())




@cli.command(short_help='Configure user settings')
def test_two_sum():
    raw_json_problem_data = fetch_problem_data("two-sum")
    parsed_problem = parse_problem_data(raw_json_problem_data)
    formatted_data = ProblemFormatter(parsed_problem)


    print(formatted_data.title)
    print(formatted_data.topic_tags)
    print(formatted_data.languages)
    print(formatted_data.description)
    print(formatted_data.examples)
    print(formatted_data.constraints)


def main():
    cli()
