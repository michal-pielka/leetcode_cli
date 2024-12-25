import click
from leetcode_cli.utils.theme_utils import (
    list_themes,
    set_current_theme,
    get_current_theme,
    validate_entire_theme
)
from leetcode_cli.exceptions.exceptions import ThemeError

@click.command(short_help='change or list themes')
@click.argument('theme_name', required=False)
def theme_cmd(theme_name):
    """
    Change or list available themes.

    If theme_name is provided, set that theme as the current theme.
    Otherwise, list all available themes.
    """
    if not theme_name:
        current_theme = get_current_theme()
        themes = list_themes()

        if not themes:
            click.echo("No themes found.")
            return

        click.echo(f"Current theme: {current_theme}")
        click.echo("Available themes:")
        for t in themes:
            click.echo(f" - {t}")

        return

    # Attempt to set the new theme
    old_theme = get_current_theme()
    success = set_current_theme(theme_name)
    if not success:
        click.echo(f"Error: Theme '{theme_name}' not found.")
        return

    # Validate the newly set theme by attempting to load *all* partial theme data
    try:
        validate_entire_theme()
        click.echo(f"Theme set to '{theme_name}'.")
    except ThemeError as e:
        # Revert to old theme since new one is invalid
        set_current_theme(old_theme)
        click.echo(f"Error: Failed to load theme '{theme_name}'. {str(e)}")
        click.echo("Reverted to the previous theme.")
