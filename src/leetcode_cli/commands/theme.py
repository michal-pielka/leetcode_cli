import click
from leetcode_cli.utils.theme_utils import list_themes, set_current_theme

@click.command(short_help='Change or list themes')
@click.argument('theme_name', required=False)
def theme_cmd(theme_name):
    """
    Change or list available themes.
    
    If THEME_NAME is provided, set that theme as the current theme.
    Otherwise, list all available themes.
    """
    if not theme_name:
        themes = list_themes()
        if not themes:
            click.echo("No themes found.")
            return

        click.echo("Available themes:")
        for t in themes:
            click.echo(f" - {t}")

        return

    success = set_current_theme(theme_name)
    if success:
        click.echo(f"Theme set to '{theme_name}'.")

    else:
        click.echo(f"Error: Theme '{theme_name}' not found.")

