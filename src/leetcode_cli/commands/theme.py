import click

from leetcode_cli.services.theme_service import list_themes, set_current_theme, get_current_theme, load_theme_data
from leetcode_cli.exceptions.exceptions import ThemeError

@click.command(short_help='Change or list themes')
@click.argument('theme_name', required=False)
def theme_cmd(theme_name):
    """
    Show or change the current theme.
    If THEME_NAME is omitted, list available themes and show the current theme.
    If THEME_NAME is provided, attempt to set the theme in config.json.
    """
    if not theme_name:
        current = get_current_theme()
        themes = list_themes()

        click.echo(f"Current theme: {current}")
        click.echo("Available themes:")
        for t in themes:
            click.echo(f" - {t}")
        return

    success = set_current_theme(theme_name)
    if not success:
        click.echo(f"Error: Theme '{theme_name}' not found. Use 'leetcode theme' to list.")
        return

    try:
        load_theme_data()
        click.echo(f"Theme set to '{theme_name}'. It appears valid.")
    except ThemeError as e:
        click.echo(f"Warning: Theme '{theme_name}' is set, but it seems invalid:\n  {e}\n"
                   "You may need to fix its JSON or switch to another theme.")
