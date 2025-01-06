import click
import logging

from leetcode_cli.services.config_service import get_chosen_problem
from leetcode_cli.services.code_service import get_language_and_extension
from leetcode_cli.data_fetchers.problem_data_fetcher import fetch_problem_id
from leetcode_cli.data_fetchers.code_snippet_fetcher import fetch_code_snippet
from leetcode_cli.services.code_service import create_solution_file

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
    """
    
    def create_file(question_id, title_slug, lang_slug, file_extension):
        """
        Fetches the code snippet and creates the solution file.
        """
        try:
            code_data = fetch_code_snippet(title_slug, lang_slug)
            snippet_list = code_data.get('data', {}).get('question', {}).get('codeSnippets', [])
            code_str = ""
            for sn in snippet_list:
                if sn.get('langSlug') == lang_slug:
                    code_str = sn.get('code', "")
                    break

            if not code_str:
                code_str = f"# Solution for {title_slug} in {lang_slug}\n\n"

            create_solution_file(question_id, title_slug, file_extension, code_str)
            file_name = f"{question_id}.{title_slug}.{file_extension}"
            click.echo(f"Solution file '{file_name}' has been created successfully.")

        except Exception as e:
            logger.error(f"Failed to create solution file: {e}")
            click.echo(f"Error: Could not create solution file. {e}")

    def get_question_id_for_slug(title_slug: str) -> str:
        try:
            question_id_data = fetch_problem_id(title_slug)
            question_id = question_id_data['data']['question']['questionFrontendId']
            return question_id
        except KeyError:
            logger.error(f"Could not find questionFrontendId for title slug '{title_slug}'.")
            click.echo(f"Error: Invalid title slug '{title_slug}'.")
            raise
        except Exception as e:
            logger.error(f"Error fetching question ID: {e}")
            click.echo(f"Error: Could not fetch question ID. {e}")
            raise

    if not title_slug_or_id:
        title_slug = get_chosen_problem()

        if not title_slug:
            click.echo("Error: No chosen problem found. Please specify a problem or use 'leetcode show' to select one.")
            return

        lang_slug, file_extension = get_language_and_extension()
        if not lang_slug or not file_extension:
            click.echo("Error: No default language set or unsupported language.")
            return

        try:
            question_id = get_question_id_for_slug(title_slug)
            create_file(question_id, title_slug, lang_slug, file_extension)

        except Exception:
            return

    else:
        if title_slug_or_id.startswith('.'):
            file_extension = title_slug_or_id.lstrip('.').lower()
            lang_slug, file_extension = get_language_and_extension(file_extension)
            if not lang_slug:
                click.echo(f"Error: Unsupported file extension '{file_extension}'.")
                return

            title_slug = get_chosen_problem()
            if not title_slug:
                click.echo("Error: No chosen problem found. Please specify a problem or use 'leetcode show' to select one.")
                return

            try:
                question_id = get_question_id_for_slug(title_slug)
                create_file(question_id, title_slug, lang_slug, file_extension)
            except Exception:
                return

        elif '.' in title_slug_or_id:
            parts = title_slug_or_id.split('.')
            if len(parts) == 3:
                frontend_id, title_slug, file_extension = parts[0], parts[1], parts[2].lower()

                if not frontend_id.isdigit():
                    click.echo("Error: Question ID in the filename is not a digit.")
                    return
                question_id = frontend_id
                lang_slug, file_extension = get_language_and_extension(file_extension)
                if not lang_slug:
                    click.echo(f"Error: Unsupported file extension '{file_extension}'.")
                    return

                create_file(question_id, title_slug, lang_slug, file_extension)

            elif len(parts) == 2:
                title_slug, file_extension = parts[0], parts[1].lower()
                lang_slug, file_extension = get_language_and_extension(file_extension)
                if not lang_slug:
                    click.echo(f"Error: Unsupported file extension '{file_extension}'.")
                    return

                try:
                    question_id = get_question_id_for_slug(title_slug)
                    create_file(question_id, title_slug, lang_slug, file_extension)

                except Exception:
                    return

            else:
                click.echo("Error: File name format is incorrect. Expected {id}.{title_slug}.{extension} or {title_slug}.{extension}.")
                return

        else:
            title_slug = title_slug_or_id
            lang_slug, file_extension = get_language_and_extension()
            if not lang_slug or not file_extension:
                click.echo("Error: No default language set or unsupported language.")
                return

            try:
                question_id = get_question_id_for_slug(title_slug)
                create_file(question_id, title_slug, lang_slug, file_extension)

            except Exception:
                return
