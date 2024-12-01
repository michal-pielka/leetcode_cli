import click
import logging
from datetime import datetime

# Import all necessary modules and functions
from .parsers.parser_utils.leetcode_stats_parser import *
from .parsers.submission_parser import *
from .parsers.leetcode_problem_parser import *
from .parsers.leetcode_problemset_parser import *
from .parsers.leetcode_stats_parser import *

from .graphics.symbols import *
from .graphics.escape_sequences import *
from .user_utils import *
from .data_fetching.leetcode_stats import *
from .data_fetching.leetcode_problem_fetcher import *
from .data_fetching.graphql_queries import *
from .data_fetching.fetch_code_snippet import *

from .leetcode_problem.submit_problem import *
from .leetcode_problem.create_solution_file import *

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Define context settings for click to adjust help message formatting
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'], max_content_width=200)

extension_to_lang_slug = {
    "cpp": "cpp",
    "java": "java",
    "py": "python",
    "py3": "python3",
    "c": "c",
    "cs": "csharp",
    "js": "javascript",
    "ts": "typescript",
    "php": "php",
    "swift": "swift",
    "kt": "kotlin",
    "dart": "dart",
    "go": "golang",
    "rb": "ruby",
    "scala": "scala",
    "rs": "rust",
    "rkt": "racket",
    "erl": "erlang",
    "ex": "elixir"
}

lang_slug_to_extension = {
    "cpp": "cpp",
    "java": "java",
    "python": "py",
    "python3": "py3",
    "c": "c",
    "csharp": "cs",
    "javascript": "js",
    "typescript": "ts",
    "php": "php",
    "swift": "swift",
    "kotlin": "kt",
    "dart": "dart",
    "golang": "go",
    "ruby": "rb",
    "scala": "scala",
    "rust": "rs",
    "racket": "rkt",
    "erlang": "erl",
    "elixir": "ex"
}

@click.group(context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """LeetCode CLI Tool

    Manage your LeetCode activities directly from the command line.
    """
    if ctx.invoked_subcommand is None:
        click.echo(cli.get_help(ctx))

@cli.command(short_help='Configure user settings')
@click.argument('key')
@click.argument('value')
def config(key, value):
    """Configure user settings.

    KEY can be 'cookie', 'username', or 'language'.
    """
    valid_keys = ['cookie', 'username', 'language']
    if key not in valid_keys:
        logger.error(f"Invalid configuration key '{key}'. Valid keys are: {', '.join(valid_keys)}.")
        click.echo(f"Error: Invalid configuration key '{key}'. Valid keys are: {', '.join(valid_keys)}.")
        return
    try:
        if key == 'cookie':
            set_cookie(value)
            logger.info("Cookie has been set successfully.")
            click.echo("Cookie has been set successfully.")
        elif key == 'username':
            set_username(value)
            logger.info(f"Username set to '{value}'.")
            click.echo(f"Username set to '{value}'.")
        elif key == 'language':
            set_language(value)
            logger.info(f"Preferred language set to '{value}'.")
            click.echo(f"Preferred language set to '{value}'.")
    except Exception as e:
        logger.error(f"Failed to set {key}: {e}")
        click.echo(f"Error: Failed to set {key}. {e}")

@cli.command(short_help='List problems')
@click.option('--difficulty', type=click.Choice(['Easy', 'Medium', 'Hard'], case_sensitive=False), default=None, help='Filter by difficulty')
@click.option('--tags', multiple=True, help='Filter by tags (comma-separated)')
@click.option('--limit', type=int, default=50, help='Limit the number of results (default: 50)')
@click.option('--page', type=int, default=1, help='Display a specific page (default: 1)')
def list(difficulty, tags, limit, page):
    """List LeetCode problems with optional filters."""
    try:
        skip = (page - 1) * limit
        category_slug = "all-code-essentials"

        tags_list = list(tags) if tags else []

        problems_dict = LeetCodeProblemFetcher.fetch_problemset(
            tags=tags_list,
            difficulty=difficulty,
            limit=limit,
            skip=skip,
            category_slug=category_slug
        )

        if not problems_dict:
            logger.error("Failed to fetch problem list.")
            click.echo("Error: Failed to fetch problem list.")
            return

        parser = LeetCodeProblemsetParser(problems_dict)
        formatted_problems = parser.get_formatted_questions()
        click.echo(formatted_problems)

    except Exception as e:
        logger.error(f"An error occurred while listing problems: {e}")
        click.echo(f"Error: An error occurred while listing problems. {e}")

@cli.command(short_help='Show problem details')
@click.argument('title_slug_or_id')
@click.option('--include', multiple=True, type=click.Choice(
    ['title', 'tags', 'langs', 'description', 'examples', 'constraints'],
    case_sensitive=False),
    help='Sections to display (default: all). Options: title, tags, langs, description, examples, constraints'
)
def show(title_slug_or_id, include):
    """
    Show problem details for the given TITLE_SLUG_OR_ID.

    TITLE_SLUG_OR_ID can be either the problem's slug or its numerical ID.
    """
    try:
        metadata = LeetCodeProblemFetcher.fetch_problem_data(title_slug_or_id)

        if not metadata:
            logger.error(f"Failed to fetch problem data for '{title_slug_or_id}'.")
            click.echo(f"Error: Failed to fetch problem data for '{title_slug_or_id}'.")
            return

        parser = LeetCodeProblemParser(metadata)

        all_sections = {
            'title': parser.get_formatted_title,
            'tags': parser.get_formatted_topic_tags,
            'langs': parser.get_formatted_languages,
            'description': parser.get_formatted_description,
            'examples': parser.get_formatted_examples,
            'constraints': parser.get_formatted_constraints
        }

        sections_to_display = all_sections.keys() if not include else include

        invalid_sections = set(sections_to_display) - set(all_sections.keys())
        if invalid_sections:
            logger.warning(f"Invalid include sections ignored: {', '.join(invalid_sections)}")
            click.echo(f"Warning: Invalid include sections ignored: {', '.join(invalid_sections)}")

        for section in sections_to_display:
            if section in all_sections:
                content = all_sections[section]()
                if content:
                    click.echo(content)
                    click.echo()

    except Exception as e:
        logger.error(f"An error occurred while showing problem details: {e}")
        click.echo(f"Error: An error occurred while showing problem details. {e}")

@cli.command(short_help='Display user stats')
@click.argument('username', required=False)
@click.option('--include', multiple=True, type=click.Choice(['stats', 'calendar'], case_sensitive=False),
              help='Sections to display (default: all). Options: stats, calendar')
def stats(username, include):
    """
    Display LeetCode user statistics.

    Usage:
        leetcode stats
        leetcode stats USERNAME
    """
    try:
        if not username:
            username = get_username()

        if not username:
            logger.error("Username is not set. Use 'leetcode config username USERNAME' to set it.")
            click.echo("Error: Username is not set. Use 'leetcode config username USERNAME' to set it.")
            return

        include = ['stats', 'calendar'] if not include else include

        valid_sections = ['stats', 'calendar']
        sections_to_include = [section.lower() for section in include if section.lower() in valid_sections]
        invalid_sections = set(section.lower() for section in include) - set(valid_sections)
        if invalid_sections:
            logger.warning(f"Invalid include sections ignored: {', '.join(invalid_sections)}")
            click.echo(f"Warning: Invalid include sections ignored: {', '.join(invalid_sections)}")

        if 'stats' in sections_to_include:
            stats_data = fetch_leetcode_stats(username)
            if stats_data:
                formatted_stats = get_formatted_leetcode_stats(stats_data)
                click.echo("User Statistics:")
                click.echo(formatted_stats)
                click.echo()
            else:
                logger.error("Failed to fetch stats data.")
                click.echo("Error: Failed to fetch stats data.")

        if 'calendar' in sections_to_include:
            current_year = datetime.utcnow().year
            previous_year = current_year - 1

            activity_current = fetch_leetcode_activity(username, current_year)
            activity_previous = fetch_leetcode_activity(username, previous_year)

            if activity_current and activity_previous:
                joined_activity = join_and_slice_calendars(activity_previous, activity_current)
                filled_activity = fill_daily_activity(joined_activity)
                formatted_activity = get_formatted_daily_activity(filled_activity)
                click.echo("Daily Activity:")
                click.echo(formatted_activity)
            else:
                logger.error("Failed to fetch activity data.")
                click.echo("Error: Failed to fetch activity data.")

    except Exception as e:
        logger.error(f"An error occurred while fetching stats: {e}")
        click.echo(f"Error: An error occurred while fetching stats. {e}")

@cli.command(short_help='Create solution file')
@click.argument('title_slug', required=False)
def create(title_slug):
    """
    Create a solution file for the given TITLE_SLUG or ID.

    Usage:
        leetcode create two-sum
        leetcode create two-sum.py

    If no file extension is provided, the default language from the config is used.
    """
    # Map of file extensions to language slugs


    try:
        if title_slug:
            if '.' in title_slug:
                # Split the argument into title_slug and file_extension
                title_slug, file_extension = title_slug.rsplit('.', 1)
                file_extension = file_extension.lower()

                # Map the file extension to the language slug
                lang_slug = extension_to_lang_slug.get(file_extension)
                if not lang_slug:
                    logger.error(f"Unsupported file extension: '{file_extension}'.")
                    click.echo(f"Error: Unsupported file extension '{file_extension}'.")
                    return
                logger.debug(f"Parsed title_slug: {title_slug}, lang_slug: {lang_slug}")
            else:
                # Use the default language from config
                title_slug = title_slug
                lang_slug = get_language()
                file_extension = lang_slug_to_extension[lang_slug]

                if not lang_slug:
                    logger.error("File extension is not specified and no default language is set in the config.")
                    click.echo("Error: File extension is not specified and no default language is set in the config.")
                    return
                logger.debug(f"Parsed title_slug: {title_slug}, using default lang_slug: {lang_slug}")
        else:
            logger.error("TITLE_SLUG or ID is required to create a solution file.")
            click.echo("Error: TITLE_SLUG or ID is required to create a solution file.")
            return

        # Create the solution file
        create_solution_file(title_slug, lang_slug)
        logger.info(f"Solution file '{title_slug}.{file_extension}' has been created successfully.")
        click.echo(f"Solution file '{title_slug}.{file_extension}' has been created successfully.")

    except Exception as e:
        logger.error(f"Failed to create solution file: {e}")
        click.echo(f"Error: Failed to create solution file. {e}")

@cli.command(short_help='Submit a solution file')
@click.argument('file_path', required=True, type=click.Path(exists=True))
def submit(file_path):
    """
    Submit a solution file for a problem.

    Usage:
        leetcode submit 1.two-sum.py
        leetcode submit 1.two-sum.cpp

    The file_path should be in the format x.y.z where:
        x = question_id
        y = title_slug
        z = file_extension
    """
    try:
        # Verify the file exists
        if not os.path.isfile(file_path):
            logger.error(f"The file '{file_path}' does not exist.")
            click.echo(f"Error: The file '{file_path}' does not exist.")
            return

        # Extract the filename from the path
        filename = os.path.basename(file_path)

        # Split the filename into parts
        parts = filename.split('.')
        if len(parts) < 3:
            logger.error("File name format is incorrect. Expected format: x.y.z (e.g., 1.two-sum.py).")
            click.echo("Error: File name format is incorrect. Expected format: x.y.z (e.g., 1.two-sum.py).")
            return

        # Extract question_id, title_slug, and file_extension
        question_id = parts[0]
        title_slug = '.'.join(parts[1:-1])  # Handles cases where title_slug contains dots
        file_extension = parts[-1].lower()

        # Map the file extension to the language slug
        lang_slug = extension_to_lang_slug.get(file_extension)
        if not lang_slug:
            logger.error(f"Unsupported file extension: '{file_extension}'.")
            click.echo(f"Error: Unsupported file extension '{file_extension}'. Supported extensions are: {', '.join(extension_to_lang_slug.keys())}.")
            return

        logger.debug(f"Parsed file_path: {file_path}")
        logger.debug(f"Question ID: {question_id}")
        logger.debug(f"Title Slug: {title_slug}")
        logger.debug(f"Language Slug: {lang_slug}")

        # Retrieve user configuration
        cookie = get_cookie()
        csrf_token = extract_csrf_token(cookie)

        if not cookie or not csrf_token:
            logger.error("Authentication tokens are missing. Please configure your 'cookie' and 'csrf_token' using the 'config' command.")
            click.echo("Error: Authentication tokens are missing. Please configure your 'cookie' and 'csrf_token' using the 'config' command.")
            return

        # Submit the solution and get the result
        result = submit_and_get_result(cookie, csrf_token, title_slug, question_id, file_path)

        if result:
            click.echo(get_formatted_submission(result))
        else:
            logger.error("Submission failed. No response received.")
            click.echo("Error: Submission failed. No response received.")

    except Exception as e:
        logger.error(f"Failed to submit solution file: {e}")
        click.echo(f"Error: Failed to submit solution file. {e}")

if __name__ == '__main__':
    cli()
