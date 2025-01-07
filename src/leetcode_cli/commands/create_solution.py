import click
import logging

from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.managers.code_manager import CodeManager
from leetcode_cli.managers.problem_manager import ProblemManager
from leetcode_cli.exceptions.exceptions import ConfigError, CodeError, ProblemError

logger = logging.getLogger(__name__)

@click.command(short_help='Create a solution file for a LeetCode problem')
@click.argument('title_slug_or_id', required=False, metavar='TITLE_SLUG_OR_ID')
def create_cmd(title_slug_or_id):
    """
    Create a solution file for the specified LeetCode problem.

    Usage Examples:
      - Create a solution for the last problem with default language: leetcode create
      - Create a solution for the last problem with a specific file extension: leetcode create .cpp
      - Create a solution by specifying title slug with extension: leetcode create two-sum.py
      - Create a solution by specifying question ID with title slug and extension: leetcode create 1.two-sum.py
      - Create a solution by specifying title slug with default language: leetcode create two-sum
      - Create a solution by specifying frontend question ID with default language: leetcode create 1
      - Create a solution by specifying frontend question ID and language extension: leetcode create 1.cpp
    """
    try:
        # Initialize managers
        config_manager = ConfigManager()
        code_manager = CodeManager(config_manager)
        problem_manager = ProblemManager(config_manager)

        # If user passes nothing => use the chosen problem from config
        is_id = title_slug_or_id.isdigit() if title_slug_or_id else False

        # Prepare placeholders
        title_slug = None
        frontend_id = None
        lang_slug = None
        file_extension = None

        if not title_slug_or_id:
            # No argument => use the chosen problem from config
            title_slug = config_manager.get_chosen_problem()
            if not title_slug:
                click.echo("Error: No chosen problem found. Please specify a problem or use 'leetcode show' to select one.")
                return

            # Get default language + extension from config
            lang_slug, file_extension = code_manager.get_language_and_extension()
            if not lang_slug or not file_extension:
                click.echo("Error: No default language set or unsupported language.")
                return

            try:
                # We want the *frontend question ID* when we only have a slug
                frontend_id = problem_manager.get_problem_frontend_id(title_slug)

                code_manager.create_solution_file_with_snippet(frontend_id, title_slug, lang_slug, file_extension)
                file_name = f"{frontend_id}.{title_slug}.{file_extension}"
                click.echo(f"Solution file '{file_name}' has been created successfully.")
            except (ProblemError, CodeError) as e:
                click.echo(f"Error: {e}")
                return

        else:
            # If user typed something
            if title_slug_or_id.startswith('.'):
                # Example: ".cpp"
                file_extension = title_slug_or_id.lstrip('.').lower()
                lang_slug, file_extension = code_manager.get_language_and_extension(file_extension)
                if not lang_slug:
                    click.echo(f"Error: Unsupported file extension '{file_extension}'.")
                    return

                # Must have a chosen problem in config
                title_slug = config_manager.get_chosen_problem()
                if not title_slug:
                    click.echo("Error: No chosen problem found. Please specify a problem or use 'leetcode show' to select one.")
                    return

                try:
                    # For the chosen slug, get *frontend ID*
                    frontend_id = problem_manager.get_problem_frontend_id(title_slug)

                    code_manager.create_solution_file_with_snippet(frontend_id, title_slug, lang_slug, file_extension)
                    file_name = f"{frontend_id}.{title_slug}.{file_extension}"
                    click.echo(f"Solution file '{file_name}' has been created successfully.")
                except (ProblemError, CodeError) as e:
                    click.echo(f"Error: {e}")
                    return

            elif '.' in title_slug_or_id:
                # Possibly: {frontend_id}.{title_slug}.{extension} OR {title_slug}.{extension} OR {frontend_id}.{extension}
                parts = title_slug_or_id.split('.')

                # e.g.: "1.two-sum.py"
                if len(parts) == 3 and parts[0].isdigit():
                    # Format => {frontend_id}.{title_slug}.{extension}
                    frontend_id, title_slug, file_extension = parts[0], parts[1], parts[2].lower()
                    lang_slug, file_extension = code_manager.get_language_and_extension(file_extension)
                    if not lang_slug:
                        click.echo(f"Error: Unsupported file extension '{file_extension}'.")
                        return

                    try:
                        code_manager.create_solution_file_with_snippet(frontend_id, title_slug, lang_slug, file_extension)
                        file_name = f"{frontend_id}.{title_slug}.{file_extension}"
                        click.echo(f"Solution file '{file_name}' has been created successfully.")
                    except (ProblemError, CodeError) as e:
                        click.echo(f"Error: {e}")
                        return

                # e.g.: "123.py"
                elif len(parts) == 2 and parts[0].isdigit():
                    # Format => {frontend_id}.{extension}
                    frontend_id, file_extension = parts[0], parts[1].lower()
                    lang_slug, file_extension = code_manager.get_language_and_extension(file_extension)
                    if not lang_slug:
                        click.echo(f"Error: Unsupported file extension '{file_extension}'.")
                        return

                    try:
                        title_slug = problem_manager.get_title_slug_for_id(frontend_id)
                        code_manager.create_solution_file_with_snippet(frontend_id, title_slug, lang_slug, file_extension)
                        file_name = f"{frontend_id}.{title_slug}.{file_extension}"
                        click.echo(f"Solution file '{file_name}' has been created successfully.")
                    except (ProblemError, CodeError) as e:
                        click.echo(f"Error: {e}")
                        return

                else:
                    # e.g.: "two-sum.py"
                    # Format => {title_slug}.{extension}
                    title_slug, file_extension = parts[0], parts[1].lower()
                    lang_slug, file_extension = code_manager.get_language_and_extension(file_extension)
                    if not lang_slug:
                        click.echo(f"Error: Unsupported file extension '{file_extension}'.")
                        return

                    try:
                        # If we only have the slug, we need the *frontend question ID* 
                        frontend_id = problem_manager.get_problem_frontend_id(title_slug)
                        code_manager.create_solution_file_with_snippet(frontend_id, title_slug, lang_slug, file_extension)
                        file_name = f"{frontend_id}.{title_slug}.{file_extension}"
                        click.echo(f"Solution file '{file_name}' has been created successfully.")
                    except (ProblemError, CodeError) as e:
                        click.echo(f"Error: {e}")
                        return

            elif is_id:
                # e.g.: "123"
                frontend_id = title_slug_or_id

                try:
                    # For an integer, we do the normal approach: no need to ask for get_problem_frontend_id,
                    # because the user already typed the front ID. We just fetch the slug from the ID.
                    title_slug = problem_manager.get_title_slug_for_id(frontend_id)
                except ProblemError as e:
                    click.echo(f"Error: {e}")
                    return

                # Then get default language
                lang_slug, file_extension = code_manager.get_language_and_extension()
                if not lang_slug or not file_extension:
                    click.echo("Error: No default language set or unsupported language.")
                    return

                try:
                    code_manager.create_solution_file_with_snippet(frontend_id, title_slug, lang_slug, file_extension)
                    file_name = f"{frontend_id}.{title_slug}.{file_extension}"
                    click.echo(f"Solution file '{file_name}' has been created successfully.")
                except (ProblemError, CodeError) as e:
                    click.echo(f"Error: {e}")
                    return

            elif '.' in title_slug_or_id and not title_slug_or_id.split('.')[0].isdigit():
                # e.g.: "two-sum.py" (already handled above if len(parts)==2)
                # If it has multiple dots or invalid format, fallback
                parts = title_slug_or_id.split('.')
                if len(parts) == 2:
                    # This was handled above in the else block
                    # but if we get here, maybe the name is weird
                    click.echo("Error: Unexpected branch. Possibly an invalid format.")
                else:
                    click.echo("Error: File name format is incorrect. Expected {id}.{title_slug}.{extension} or {title_slug}.{extension}.")
                return

            else:
                # e.g.: "two-sum" (slug only, no extension)
                title_slug = title_slug_or_id
                lang_slug, file_extension = code_manager.get_language_and_extension()
                if not lang_slug or not file_extension:
                    click.echo("Error: No default language set or unsupported language.")
                    return

                try:
                    # We only have the slug => retrieve the frontend ID
                    frontend_id = problem_manager.get_problem_frontend_id(title_slug)
                    code_manager.create_solution_file_with_snippet(frontend_id, title_slug, lang_slug, file_extension)
                    file_name = f"{frontend_id}.{title_slug}.{file_extension}"
                    click.echo(f"Solution file '{file_name}' has been created successfully.")
                except (ProblemError, CodeError) as e:
                    click.echo(f"Error: {e}")
                    return

    except ConfigError as e:
        logger.error(e)
        click.echo(f"Configuration Error: {e}", err=True)
    except Exception as e:
        logger.exception("An unexpected error occurred during solution creation.")
        click.echo("An unexpected error occurred. Please try again.", err=True)
