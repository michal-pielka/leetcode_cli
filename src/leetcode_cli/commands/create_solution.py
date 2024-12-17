# leetcode_cli/commands/create_solution.py
import click


from leetcode_cli.utils.config_utils import get_chosen_problem
from leetcode_cli.utils.download_problems_utils import load_problems_metadata, get_problem_by_key_value
from leetcode_cli.utils.code_utils import get_language_and_extension
from leetcode_cli.data_fetching.problem_fetcher import fetch_problem_id
from leetcode_cli.data_fetching.code_snippet_fetcher import fetch_code_snippet
from leetcode_cli.leetcode_problem.create_solution_file import create_solution_file

@click.command(short_help='Create solution file')
@click.argument('title_slug_or_id', required=False)
def create_cmd(title_slug_or_id):
    """
    Create a solution file for the given TITLE_SLUG or ID.

    If no argument is given, uses chosen problem and default language.
    If argument given with extension, uses that extension.
    Otherwise tries to map default language to extension.

    Possible cases:
    1) No argument: Use chosen problem and default language.
    2) Argument starts with '.' (e.g. ".cpp"): Use chosen problem and provided extension.
    3) Argument has '.' inside (e.g. "two-sum.py" or "1.two-sum.py"):
       - If "1.two-sum.py": question_id=1, title_slug="two-sum"
       - If "two-sum.py": title_slug="two-sum", fetch question_id
    4) Argument no dot (e.g. "two-sum"): Just a slug, use default language and fetch question_id.
    """

    def create_file(question_id, title_slug, lang_slug, file_extension):
        # Fetch code snippet data
        code_data = fetch_code_snippet(title_slug, lang_slug)
        # Extract the code snippet string
        snippet_list = code_data.get('data', {}).get('question', {}).get('codeSnippets', [])
        code_str = ""
        for sn in snippet_list:
            if sn.get('langSlug') == lang_slug:
                code_str = sn.get('code', "")
                break

        if not code_str:
            # If no snippet found for this language, fallback to a default comment
            code_str = f"# {title_slug} solution in {lang_slug}\n\n"

        # Create solution file (question_id.title_slug.file_extension)
        create_solution_file(question_id, title_slug, file_extension, code_str)
        file_name = f"{question_id}.{title_slug}.{file_extension}"
        click.echo(f"Solution file '{file_name}' has been created successfully.")

    def get_question_id_for_slug(title_slug: str) -> str:
        # fetch_problem_id returns a dict like {'data': {'question': {'questionFrontendId': '3000'}}}
        question_id_data = fetch_problem_id(title_slug)
        # Extract the frontend question ID as a string
        question_id = question_id_data['data']['question']['questionFrontendId']
        return question_id

    # Case 1: No argument
    if not title_slug_or_id:
        title_slug = get_chosen_problem()
        if not title_slug:
            click.echo("Error: No chosen problem found. Please specify a problem or 'leetcode show' to select one.")
            return

        lang_slug, file_extension = get_language_and_extension()
        if not lang_slug or not file_extension:
            click.echo("Error: No default language set or unsupported language.")
            return

        question_id = get_question_id_for_slug(title_slug)
        create_file(question_id, title_slug, lang_slug, file_extension)
        return

    # Case 2: Argument starts with '.' (extension only)
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

        question_id = get_question_id_for_slug(title_slug)
        create_file(question_id, title_slug, lang_slug, file_extension)
        return

    # Case 3: Argument has '.' inside
    if '.' in title_slug_or_id:
        parts = title_slug_or_id.split('.')
        if len(parts) == 3:
            # Format: question_id.title_slug.extension
            frontend_id, title_slug, file_extension = parts[0], parts[1], parts[2].lower()

            if not frontend_id.isdigit():
                click.echo("Error: Question ID in the filename is not a digit.")
                return
            question_id = frontend_id
            lang_slug, file_extension = get_language_and_extension(file_extension)
            if not lang_slug:
                click.echo(f"Error: Unsupported file extension '{file_extension}'.")
                return

        elif len(parts) == 2:
            # Format: title_slug.extension
            title_slug, file_extension = parts[0], parts[1].lower()
            lang_slug, file_extension = get_language_and_extension(file_extension)
            if not lang_slug:
                click.echo(f"Error: Unsupported file extension '{file_extension}'.")
                return
            question_id = get_question_id_for_slug(title_slug)
        else:
            # Unexpected format
            click.echo("Error: File name format is incorrect. Expected {id}.{title_slug}.{extension} or {title_slug}.{extension}")
            return

        create_file(question_id, title_slug, lang_slug, file_extension)
        return

    # Case 4: Argument has no dot
    if title_slug_or_id.isdigit():
        problems_data = load_problems_metadata()
        if not problems_data:
            click.echo("Error: problems' metadata not found, use leetcode download-problems.")
            return

        selected_problem = get_problem_by_key_value(problems_data, "frontendQuestionId", title_slug_or_id)
        title_slug = selected_problem.get("titleSlug", None)

        if not title_slug:
            click.echo("Error: no problem for specified id in problems' metadata.")
            return

        lang_slug, file_extension = get_language_and_extension()
        create_file(title_slug_or_id, title_slug, lang_slug, file_extension)

        return
    else:
        # It's a slug
        title_slug = title_slug_or_id
        lang_slug, file_extension = get_language_and_extension()
        if not lang_slug or not file_extension:
            click.echo("Error: No default language set or unsupported language.")
            return

        question_id = get_question_id_for_slug(title_slug)
        create_file(question_id, title_slug, lang_slug, file_extension)
