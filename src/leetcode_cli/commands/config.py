# leetcode_cli/commands/config.py
import click
from leetcode_cli.graphics.ansi_codes import ANSI_RESET, ANSI_CODES
from leetcode_cli.core.config_service import set_cookie, set_username, set_language

valid_keys = ['cookie', 'username', 'language']

@click.command(short_help='Configure user settings')
@click.argument('key')
@click.argument('value')
def config_cmd(key, value):
    """
    Configure user settings.

    KEY can be 'cookie', 'username', or 'language'.
    """
    if key not in valid_keys:
        click.echo(f"Error: Invalid configuration key {ANSI_CODES['ITALIC']}{key}{ANSI_RESET}. Valid keys: {', '.join(valid_keys)}")
        return

    if key == 'cookie':
        set_cookie(value)
        click.echo("Cookie set successfully.")

    elif key == 'username':
        set_username(value)
        click.echo(f"Username set to {ANSI_CODES['ITALIC']}{value}{ANSI_RESET}.")

    elif key == 'language':
        set_language(value)
        click.echo(f"Preferred language set to {ANSI_CODES['ITALIC']}{value}{ANSI_RESET}.")
