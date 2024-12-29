# commands/theme.py
import click
from leetcode_cli.utils.theme_utils import list_themes, set_current_theme, get_current_theme, validate_entire_theme
from leetcode_cli.exceptions.exceptions import ThemeError

@click.command(short_help='Change or list themes')
@click.argument('theme_name', required=False)
def theme_cmd(theme_name):
    """
    Change or list available themes.
    If theme_name is provided, set that theme as current and validate it.
    Otherwise, list all available themes.
    """
    if not theme_name:
        # List themes
        current = get_current_theme()
        themes = list_themes()
        if not themes:
            click.echo("No themes found.")
            return
        click.echo(f"Current theme: {current}")
        click.echo("Available themes:")
        for t in themes:
            click.echo(f" - {t}")
        return
    
    # Attempt to set new theme
    if not set_current_theme(theme_name):
        click.echo(f"Error: Theme '{theme_name}' not found.")
        return
    
    # Validate
    try:
        validate_entire_theme()
        click.echo(f"Theme set to '{theme_name}'. Validation succeeded.")
    except ThemeError as e:
        # revert if wanted
        click.echo(f"Error: {e}")
        # Optionally revert
        # set_current_theme(old_theme)
