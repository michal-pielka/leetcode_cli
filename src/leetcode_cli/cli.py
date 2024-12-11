# leetcode_cli/cli.py
import logging
import click

# Import command groups from separate files
from leetcode_cli.commands.config import config_cmd
from leetcode_cli.commands.list_problems import list_cmd
from leetcode_cli.commands.show_problem import show_cmd
from leetcode_cli.commands.submit import submit_cmd
from leetcode_cli.commands.test_solution import test_cmd
from leetcode_cli.commands.download_problems import download_problems_cmd
from leetcode_cli.commands.stats import stats_cmd
from leetcode_cli.commands.create_solution import create_cmd

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

@click.group(context_settings=dict(help_option_names=['-h', '--help'], max_content_width=200))
@click.pass_context
def cli(ctx):
    """
    LeetCode CLI Tool

    Manage your LeetCode activities directly from the command line.
    """
    if ctx.invoked_subcommand is None:
        click.echo(cli.get_help(ctx))

# Add subcommands from separate command modules
cli.add_command(config_cmd, "config")
cli.add_command(list_cmd, "list")
cli.add_command(show_cmd, "show")
cli.add_command(submit_cmd, "submit")
cli.add_command(test_cmd, "test")
cli.add_command(download_problems_cmd, "download-problems")
cli.add_command(stats_cmd, "stats")
cli.add_command(create_cmd, "create")

def main():
    configure_logging()
    cli()

if __name__ == "__main__":
    main()
