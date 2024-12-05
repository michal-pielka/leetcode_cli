from os.path import exists
import click
import time
import json
import logging
import os
from datetime import datetime

from leetcode_cli.graphics.symbols import SYMBOLS
from leetcode_cli.graphics.escape_sequences import ANSI_RESET, ANSI_CODES

from leetcode_cli.parsers.submission_parser import get_formatted_submission, get_formatted_interpretation, SubmissionParseError
from leetcode_cli.parsers.problem_parser import LeetCodeProblemParser, LeetCodePaidOnlyProblemError
from leetcode_cli.parsers.problemset_parser import LeetCodeProblemsetParser
from leetcode_cli.parsers.stats_parser import get_formatted_leetcode_stats, get_formatted_daily_activity
from leetcode_cli.parsers.parser_utils.stats_parser_utils import *

from leetcode_cli.user_utils import (
    get_problem_by_key_value,
    set_chosen_problem,
    get_chosen_problem,
    filter_problems,
    get_problems_data_path,
    select_random_problem,
    get_cookie,
    get_username,
    get_language,
    extract_csrf_token,
    set_cookie,
    set_username,
    set_language,
    problem_data_from_path,
    load_problems_metadata
)

from leetcode_cli.data_fetching.stats_fetcher import fetch_user_stats, fetch_user_activity
from leetcode_cli.data_fetching.problem_fetcher import fetch_problem_data, fetch_problem_testcases
from leetcode_cli.data_fetching.problemset_fetcher import fetch_problemset
from leetcode_cli.data_fetching.code_snippet_fetcher import CodeSnippetFetchError

from leetcode_cli.leetcode_problem.problem_submitter import interpret_and_get_result, interpret_solution
from leetcode_cli.leetcode_problem.problem_submitter import submit_and_get_result, SubmissionError
from leetcode_cli.leetcode_problem.solution_file_creator import create_solution_file

# Configure logging
def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

logger = logging.getLogger(__name__)
logging.disable(logging.CRITICAL)

# Define context settings for click to adjust help message formatting
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'], max_content_width=200)

POSSIBLE_LANG_SLUGS = ["cpp", "java", "python", "python3", "c", "csharp", "javascript", "typescript", "php", "swift", "kotlin", "dart", "golang", "ruby", "scala", "rust", "racket", "erlang", "elixir"]
POSSIBLE_FILE_EXTENSIONS = ["cpp", "java", "py", "py3", "c", "cs", "js", "ts", "php", "swift", "kt", "dart", "go", "rb", "scala", "rs", "rkt", "erl", "ex"]

POSSIBLE_TAGS = [
    "array",
    "string",
    "hash-table",
    "dynamic-programming",
    "math",
    "sorting",
    "greedy",
    "depth-first-search",
    "binary-search",
    "database",
    "matrix",
    "tree",
    "breadth-first-search",
    "bit-manipulation",
    "two-pointers",
    "prefix-sum",
    "heap-priority-queue",
    "binary-tree",
    "simulation",
    "stack",
    "counting",
    "graph",
    "sliding-window",
    "design",
    "backtracking",
    "enumeration",
    "union-find",
    "linked-list",
    "ordered-set",
    "number-theory",
    "monotonic-stack",
    "trie",
    "segment-tree",
    "bitmask",
    "queue",
    "divide-and-conquer",
    "recursion",
    "combinatorics",
    "binary-search-tree",
    "hash-function",
    "memoization",
    "binary-indexed-tree",
    "geometry",
    "string-matching",
    "topological-sort",
    "shortest-path",
    "rolling-hash",
    "game-theory",
    "interactive",
    "data-stream",
    "monotonic-queue",
    "brainteaser",
    "randomized",
    "merge-sort",
    "doubly-linked-list",
    "counting-sort",
    "iterator",
    "concurrency",
    "probability-and-statistics",
    "quickselect",
    "suffix-array",
    "bucket-sort",
    "minimum-spanning-tree",
    "shell",
    "line-sweep",
    "reservoir-sampling",
    "strongly-connected-component",
    "eulerian-circuit",
    "radix-sort",
    "rejection-sampling",
    "biconnected-component"
]

extension_to_lang_slug = {
    POSSIBLE_FILE_EXTENSIONS[i]: POSSIBLE_LANG_SLUGS[i] for i in range(len(POSSIBLE_LANG_SLUGS))
}

lang_slug_to_extension = {
    POSSIBLE_LANG_SLUGS[i]: POSSIBLE_FILE_EXTENSIONS[i] for i in range(len(POSSIBLE_FILE_EXTENSIONS))
}


def get_language_and_extension(file_extension=None):
    if file_extension:
        # Map the file extension to the language slug
        lang_slug = extension_to_lang_slug.get(file_extension.lower())
        if not lang_slug:
            click.echo(f"Error: Unsupported file extension '{file_extension}'. Supported extensions are: {', '.join(extension_to_lang_slug.keys())}.")
            return None, None
    else:
        # Fetch the default language from config
        lang_slug = get_language()
        if not lang_slug or lang_slug.lower() not in POSSIBLE_LANG_SLUGS:
            click.echo("Error: No default language set or unsupported language. Use 'leetcode config language LANG' to set it.")
            return None, None

        # Map the language slug to the file extension
        file_extension = lang_slug_to_extension.get(lang_slug.lower())
        if not file_extension:
            click.echo(f"Error: Unsupported language slug '{lang_slug}'. Please check your configuration.")
            return None, None

    return lang_slug, file_extension


def extract_question_info(problem_data):
    try:
        question = problem_data['data']['question']
        question_id = question['frontendQuestionId']
        title_slug = question['titleSlug']
        return question_id, title_slug
    except KeyError as e:
        raise Exception(f"Invalid problem data structure received: missing key {e}")




def find_problem_by_id(problems_data, problem_id):
    """
    Finds a problem by its frontendQuestionId in the problems data.

    Args:
        problems_data (dict): The problems metadata.
        problem_id (str): The problem's frontendQuestionId.

    Returns:
        dict: The problem data if found, None otherwise.
    """
    questions = problems_data.get('data', {}).get('problemsetQuestionList', {}).get('questions', [])
    problem_data = next((q for q in questions if q.get('frontendQuestionId') == problem_id), None)
    return problem_data


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
    """
    Configure user settings.

    KEY can be 'cookie', 'username', or 'language'.
    """

    valid_keys = ['cookie', 'username', 'language']

    if key not in valid_keys:
        logger.error(f"Invalid configuration key '{key}'. Valid keys are: {', '.join(valid_keys)}.")
        click.echo(f"Error: Invalid configuration key {ANSI_CODES['ITALIC']}{key}{ANSI_RESET}. Valid keys are: {ANSI_CODES['ITALIC']}{', '.join(valid_keys)}{ANSI_RESET}.")
        return

    if key == 'cookie':
        set_cookie(value)
        logger.info("Cookie has been set successfully.")
        click.echo("Cookie has been set successfully.")

    elif key == 'username':
        set_username(value)
        logger.info(f"Username set to '{value}'.")
        click.echo(f"Username set to {ANSI_CODES['ITALIC']}{value}{ANSI_RESET}.")

    elif key == 'language':
        if value not in POSSIBLE_LANG_SLUGS:
            click.echo("Incorrect language, choose from these:")
            for lang in POSSIBLE_LANG_SLUGS:
                click.echo(f"  {lang}")
            return

        set_language(value)
        logger.info(f"Preferred language set to '{value}'.")
        click.echo(f"Preferred language set to {ANSI_CODES['ITALIC']}{value}{ANSI_RESET}.")




def validate_integer(ctx, param, value):
    if value <= 0:
        raise click.BadParameter('Limit must be greater than 0.')
    return value





@cli.command(short_help='List problems')
@click.option(
    '--difficulty',
    type=click.Choice(["EASY", "MEDIUM", "HARD"], case_sensitive=False),
    help='Filter by difficulty.'
)
@click.option(
    '--tag',
    multiple=True,
    type=click.Choice(POSSIBLE_TAGS, case_sensitive=False),
    help='Filter by tag. Multiple tags can be specified.'
)
@click.option(
    '--limit',
    type=int,
    default=50,
    help='Limit the number of results (default: 50)',
    callback=validate_integer
)
@click.option(
    '--page',
    type=int,
    default=1,
    help='Display a specific page (default: 1)',
    callback=validate_integer
)
@click.option(
    '--use-downloaded',
    is_flag=True,
    help='Use downloaded problems metadata from local storage.'
)
def list(difficulty, tag, limit, page, use_downloaded):
    """List LeetCode problems with optional filters."""
    logger.debug("Starting 'list' command with parameters:")
    logger.debug(f"Difficulty: '{difficulty}'")
    logger.debug(f"Tags: {tag}")
    logger.debug(f"Limit: {limit}")
    logger.debug(f"Page: {page}")
    logger.debug(f"Use downloaded: {use_downloaded}")

    skip = (page - 1) * limit

    if use_downloaded:
        problems_data = load_problems_metadata()
        if not problems_data:
            return

        # Filter problems
        filtered_problems = filter_problems(problems_data, difficulty, tag)
        if not filtered_problems:
            click.echo("Error: No problems found with the specified filters.")
            return

        if skip >= len(filtered_problems):
            click.echo("Error: No problems at this page, try using a lower value.")
            return

        problems_list = filtered_problems[skip:skip+limit]

        # Prepare data for the parser
        problems_dict = {
            'data': {
                'problemsetQuestionList': {
                    'questions': problems_list
                }
            }
        }

    else:
        # Fetch cookie and CSRF token
        cookie = get_cookie()
        csrf_token = extract_csrf_token(cookie)

        # Fetch problemset
        problems_dict = fetch_problemset(
            cookie=cookie,
            csrf_token=csrf_token,
            tags=tag,
            difficulty=difficulty,
            limit=limit,
            skip=skip,
        )

        logger.debug(f"Fetched Problems: {problems_dict}")

    if not problems_dict or not problems_dict['data']['problemsetQuestionList']['questions']:
        click.echo("Error: No problems found with the specified filters.")
        return

    parser = LeetCodeProblemsetParser(problems_dict)
    formatted_problems = parser.get_formatted_questions()
    click.echo(formatted_problems)
    click.echo()


"""
def validate_bounds(ctx, param, value):
    if value <= 0:
        raise click.BadParameter('Limit must be greater than 0.')
    return value
"""

"""
maybe implement this??

@click.option(
    '--lower',
    type=int,
    default=0,
    help='Set the lower questionID bound when showing random problem (Requires --random).',
    callback=validate_bounds
)
@click.option(
    '--upper',
    type=int,
    default=0,
    help='Set the lower questionID bound when showing random problem (Requires --random).',
    callback=validate_bounds
)
"""





@cli.command(short_help='Show problem details')
@click.argument('title_slug_or_id', required=False)
@click.option(
    '--include',
    multiple=True,
    type=click.Choice([
        "title", "tags", "langs", "description",
        "examples", "constraints"
    ], case_sensitive=False),
    help='Sections to display (default: all). Options: title, tags, langs, description, examples, constraints'
)
@click.option(
    '--random',
    is_flag=True,
    help='Show a random problem'
)
@click.option(
    '--difficulty',
    type=click.Choice(["EASY", "MEDIUM", "HARD"], case_sensitive=False),
    help='Filter random problems by difficulty (Requires --random)'
)
@click.option(
    '--tag',
    multiple=True,
    type=click.Choice(POSSIBLE_TAGS, case_sensitive=False),
    help='Filter random problems by tag (Requires --random). Multiple tags can be specified'
)
@click.option(
    '--use-downloaded',
    is_flag=True,
    help='Use downloaded problems metadata from local storage'
)
def show(title_slug_or_id, include, random, difficulty, tag, use_downloaded):
    problem_data = None
    title_slug = None

    # Enforce that --difficulty and --tag can only be used with --random
    if (difficulty or tag) and not random:
        click.echo(f"Error: {ANSI_CODES['ITALIC']}--difficulty{ANSI_RESET}, {ANSI_CODES['ITALIC']}--tag{ANSI_RESET}, {ANSI_CODES['ITALIC']}--lower{ANSI_RESET} and {ANSI_CODES['ITALIC']}--upper{ANSI_RESET}  options can only be used with {ANSI_CODES['ITALIC']}--random{ANSI_RESET}.")
        return


    if random:
        if use_downloaded:
            problems_data = load_problems_metadata()

            if not problems_data:
                click.echo(f"Error: Failed to fetch problem list.")
                return

            filtered_problems = filter_problems(problems_data, difficulty, tag)
        else:
            # Fetch problems from LeetCode API
            cookie = get_cookie()
            csrf_token = extract_csrf_token(cookie)

            # Fetch problemset
            filtered_problems_data = fetch_problemset(
                cookie=cookie,
                csrf_token=csrf_token,
                tags=tag,
                difficulty=difficulty,
                limit=100000,
                skip=0,
            )

            filtered_problems = filtered_problems_data.get('data', {}).get('problemsetQuestionList', {}).get('questions', {})
            

        if not filtered_problems:
            click.echo("Error: No matching problem found with the specified filters.")
            return

        # Select a random problem
        problem_data = select_random_problem(filtered_problems)

        title_slug = problem_data.get('titleSlug')
        if not title_slug:
            click.echo("Error: Selected problem does not have a 'titleSlug'.")
            return


    else:
        if use_downloaded:
            problems_data = load_problems_metadata()

            # Assume user provided title-slug
            problem_data = get_problem_by_key_value(problems_data, "titleSlug", title_slug_or_id)

            if not problem_data:
                # Assumption was wrong, user provided ID
                problem_data = get_problem_by_key_value(problems_data, "frontendQuestionId", title_slug_or_id)

            if not problem_data:
                click.echo(f"Error: Problem with titleSlug or questionID '{title_slug_or_id}' not found in cached data.")
                return

            title_slug = problem_data.get('titleSlug', None)

        else:
            if title_slug_or_id.isdigit():
                click.echo("Error: Problems' metadata not found. Please use leetcode download-problems or use title slug instead of ID.")
                return

            else:
                title_slug = title_slug_or_id

    metadata = fetch_problem_data(title_slug)

    if not metadata or not metadata['data']['question']:
        click.echo(f"Error: Can't fetch problem: {title_slug_or_id}")
        return

    # Update the config file
    set_chosen_problem(title_slug)

    try:
        parser = LeetCodeProblemParser(metadata)
        all_sections = {
            'title': parser.get_formatted_title,
            'tags': parser.get_formatted_topic_tags,
            'langs': parser.get_formatted_languages,
            'description': parser.get_formatted_description,
            'examples': parser.get_formatted_examples,
            'constraints': parser.get_formatted_constraints
        }

        if not include:
            sections_to_display = all_sections.keys()
        else:
            sections_to_display = include

        for section in sections_to_display:
            if section in all_sections:
                content = all_sections[section]()
                if content:
                    click.echo(content)
                    click.echo()

    except LeetCodePaidOnlyProblemError as e:
        click.echo("Error: This is a paid-only problem and cannot be viewed without a premium subscription.")
        return


@cli.command(short_help='Display user stats')
@click.argument('username', required=False, default=get_username())
@click.option(
    '--include',
    multiple=True,
    type=click.Choice(["stats", "calendar"], case_sensitive=False),
    help='Sections to display (default: all). Options: stats, calendar'
)
def stats(username, include):
    """
    Display LeetCode user statistics.

    Usage:
        leetcode stats
        leetcode stats USERNAME
    """
    VALID_SECTIONS = ["stats", "calendar"]

    try:
        if not username:
            click.echo(f"Error: Username was not specified and is not set. Use {ANSI_CODES['ITALIC']}leetcode config username USERNAME{ANSI_RESET} to set it or {ANSI_CODES['ITALIC']}leetcode stats USERNAME{ANSI_RESET}.")
            return

        if not include:
            include = VALID_SECTIONS

        formatted_stats = None
        formatted_activity = None

        if 'stats' in include:
            stats_data = fetch_user_stats(username)

            if stats_data:
                formatted_stats = get_formatted_leetcode_stats(stats_data)
            else:
                click.echo("Error: Failed to fetch stats data.")

        if 'calendar' in include:
            current_year = datetime.now().year
            previous_year = current_year - 1

            activity_current = fetch_user_activity(username, current_year)
            activity_previous = fetch_user_activity(username, previous_year)

            if activity_current and activity_previous:
                joined_activity = join_and_slice_calendars(activity_previous, activity_current)
                filled_activity = fill_daily_activity(joined_activity)
                formatted_activity = get_formatted_daily_activity(filled_activity)
            else:
                click.echo("Error: Failed to fetch activity data.")

        # Display the fetched and formatted data
        if formatted_stats:
            click.echo()
            click.echo(formatted_stats)
            click.echo()

        if formatted_activity:
            click.echo()
            click.echo(formatted_activity)
            click.echo()

    except Exception as e:
        logger.error(f"An error occurred while fetching stats: {e}", exc_info=True)
        click.echo(f"Error: An error occurred while fetching stats. {e}")



@cli.command(short_help='Create solution file')
@click.argument('title_slug_or_id', required=False)
def create(title_slug_or_id):
    """
    Create a solution file for the given TITLE_SLUG or ID.

    Usage:
        leetcode create two-sum.py
        leetcode create two-sum
        leetcode create 1.py
        leetcode create 1
        leetcode create .cpp
        leetcode create

    If a language extension is specified, it uses that.
    If no file extension is provided, it fetches the default language from the config and maps it through lang_slug_to_extension dictionary.
    """
    logger.debug(f"Received title_slug_or_id argument: '{title_slug_or_id}'")

    try:
        if title_slug_or_id:
            if title_slug_or_id.startswith('.'):
                # **Usage:** leetcode create .cpp
                file_extension = title_slug_or_id.lstrip('.').lower()
                logger.debug(f"Extracted file_extension: '{file_extension}'")

                lang_slug, file_extension = get_language_and_extension(file_extension)
                if not lang_slug:
                    return

                # Fetch the chosen problem from config
                title_slug = get_chosen_problem()
                if not title_slug:
                    click.echo("Error: No chosen problem found in config. Please specify a problem or use 'leetcode show' to select one.")
                    return

            elif '.' in title_slug_or_id:
                # **Usage:** leetcode create two-sum.py or leetcode create 1.py
                title_slug_part, file_extension = title_slug_or_id.rsplit('.', 1)
                file_extension = file_extension.lower()
                logger.debug(f"Extracted title_slug_or_id: '{title_slug_part}', file_extension: '{file_extension}'")

                lang_slug, file_extension = get_language_and_extension(file_extension)
                if not lang_slug:
                    return

                title_slug = None
                if not title_slug:
                    return

            else:
                # **Usage:** leetcode create two-sum or leetcode create 1
                lang_slug, file_extension = get_language_and_extension()
                if not lang_slug:
                    return

                title_slug = None
                if not title_slug:
                    return
        else:
            # **Usage:** leetcode create
            # Fetch the chosen problem from config
            title_slug = get_chosen_problem()
            if not title_slug:
                click.echo("Error: No chosen problem found in config. Please specify a problem or use 'leetcode show' to select one.")
                return

            # Get default language and file extension
            lang_slug, file_extension = get_language_and_extension()
            if not lang_slug:
                return

        # Fetch problem data using the title_slug
        problem_data = fetch_problem_data(title_slug)
        if not problem_data:
            raise CodeSnippetFetchError(f"Problem data for '{title_slug}' could not be fetched.")

        # Extract question info
        question_id_fetched, title_slug_fetched = extract_question_info(problem_data)

        # Call create_solution_file with all required parameters
        create_solution_file(question_id_fetched, title_slug_fetched, lang_slug, file_extension)

        # Define the filename based on question_id, title_slug, and file_extension
        file_name = f"{question_id_fetched}.{title_slug_fetched}.{file_extension}"
        click.echo(f"Solution file '{file_name}' has been created successfully.")

    except CodeSnippetFetchError as e:
        logger.error(f"CodeSnippetFetchError: {e}")
        click.echo(f"Error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        click.echo(f"Error: {e}")



@cli.command(short_help='Test a solution file')
@click.argument('file_path', required=True, type=click.Path(exists=True))

def test(file_path):
    try:
        # Extract the filename from the path
        filename = os.path.basename(file_path)

        # Split the filename into parts
        parts = filename.split('.')
        if len(parts) < 3:
            click.echo("Error: File name format is incorrect. Expected format: x.y.z (e.g., 1.two-sum.py).")
            return

        # Retrieve user configuration
        cookie = get_cookie()
        csrf_token = extract_csrf_token(cookie)

        if not cookie or not csrf_token:
            click.echo("Error: Authentication tokens are missing. Please configure your 'cookie' using the 'config' command.")
            return

        title_slug_part, file_extension = filename.rsplit('.', 1)
        file_extension = file_extension.lower()
        logger.debug(f"Extracted title_slug_or_id: '{title_slug_part}', file_extension: '{file_extension}'")

        lang_slug, file_extension = get_language_and_extension(file_extension)
        if not lang_slug:
            return


        title_slug = title_slug_part.split(".")[1]

        problem_testcases = fetch_problem_testcases(title_slug)['data']['question']['exampleTestcases']
        result = interpret_and_get_result(cookie, csrf_token, file_path, problem_testcases)

        if result:
            formatted_result = get_formatted_interpretation(result, problem_testcases)
            click.echo(formatted_result)
        else:
            click.echo("Error: Submission failed. No response received.")

    except (SubmissionError, SubmissionParseError) as e:
        logger.error(f"Submission failed: {e}")
        click.echo(f"Error: Submission failed. {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        click.echo(f"Error: An unexpected error occurred. {e}")



@cli.command(short_help='Submit a solution file')
@click.argument('file_path', required=True, type=click.Path(exists=True))
def submit(file_path):
    """
    Submit a solution file for a problem.

    Usage:
        leetcode submit 1.two-sum.py
    """
    try:
        # Extract the filename from the path
        filename = os.path.basename(file_path)

        # Split the filename into parts
        parts = filename.split('.')
        if len(parts) < 3:
            click.echo("Error: File name format is incorrect. Expected format: x.y.z (e.g., 1.two-sum.py).")
            return

        # Retrieve user configuration
        cookie = get_cookie()
        csrf_token = extract_csrf_token(cookie)

        if not cookie or not csrf_token:
            click.echo("Error: Authentication tokens are missing. Please configure your 'cookie' using the 'config' command.")
            return

        result = submit_and_get_result(cookie, csrf_token, file_path)

        if result:
            formatted_result = get_formatted_submission(result)
            click.echo(formatted_result)
        else:
            click.echo("Error: Submission failed. No response received.")

    except (SubmissionError, SubmissionParseError) as e:
        logger.error(f"Submission failed: {e}")
        click.echo(f"Error: Submission failed. {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        click.echo(f"Error: An unexpected error occurred. {e}")


@cli.command(short_help='Download all problems metadata')
def download_problems():
    """
    Download all LeetCode problems metadata and save it locally.

    The problems metadata will be saved to '~/.config/leetcode/problems_metadata.json'.
    """
    try:
        logger.info("Fetching all problems metadata from LeetCode...")
        # Fetch all problems
        problems_data = fetch_problemset(
            cookie=None,
            csrf_token=None,
            tags=None,
            difficulty=None,
            limit=100000,
            skip=0,
        )

        if not problems_data:
            click.echo("Error: Failed to fetch problems metadata.")
            return

        # Determine the path to save the problems metadata
        problems_path = get_problems_data_path()

        # Save the problems data to the specified path
        os.makedirs(os.path.dirname(problems_path), exist_ok=True)
        with open(problems_path, "w") as f:
            json.dump(problems_data, f, indent=4)
        logger.info(f"Problems metadata saved to {problems_path}")
        click.echo(f"Problems metadata has been downloaded and saved to '{problems_path}'.")
    except Exception as e:
        logger.error(f"An error occurred while downloading problems metadata: {e}", exc_info=True)
        click.echo(f"Error: An error occurred while downloading problems metadata. {e}")


@cli.command(short_help="TEST SOME CODE // REMOVE LATER")
def test1():
    def test_every_submission_parse():
        #result = submit_and_get_result(cookie, csrf_token, title_slug, question_id, file_path)
        results_possible = {
            "result_accepted" : {'status_code': 10, 'lang': 'python', 'run_success': True, 'status_runtime': '7 ms', 'memory': 12008000, 'display_runtime': '7', 'question_id': '409', 'elapsed_time': 46, 'compare_result': '1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111', 'code_output': '', 'std_output': '', 'last_testcase': '', 'expected_output': '', 'task_finish_time': 1733121005250, 'task_name': 'judger.judgetask.Judge', 'finished': True, 'total_correct': 97, 'total_testcases': 97, 'runtime_percentile': 17.433899999999994, 'status_memory': '12 MB', 'memory_percentile': 5.559299999999997, 'pretty_lang': 'Python', 'submission_id': '1468060198', 'status_msg': 'Accepted', 'state': 'SUCCESS'},

            "result_wrong" : {'status_code': 11, 'lang': 'python', 'run_success': True, 'status_runtime': 'N/A', 'memory': 12124000, 'display_runtime': '0', 'question_id': '409', 'elapsed_time': 33, 'compare_result': '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', 'code_output': '123', 'std_output': 'std line 1\nstd line 2\n', 'last_testcase': '"abccccdd"', 'expected_output': '7', 'task_finish_time': 1733121084175, 'task_name': 'judger.judgetask.Judge', 'finished': True, 'total_correct': 0, 'total_testcases': 97, 'runtime_percentile': None, 'status_memory': 'N/A', 'memory_percentile': None, 'pretty_lang': 'Python', 'submission_id': '1468061226', 'input_formatted': '"abccccdd"', 'input': '"abccccdd"', 'status_msg': 'Wrong Answer', 'state': 'SUCCESS'},

            "result_mle" : {'status_code': 12, 'lang': 'python', 'run_success': False, 'status_runtime': 'N/A', 'memory': 976576000, 'question_id': '409', 'elapsed_time': 399, 'compare_result': '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', 'code_output': '', 'std_output': '', 'last_testcase': '"abccccdd"', 'expected_output': '7', 'task_finish_time': 1733121307119, 'task_name': 'judger.judgetask.Judge', 'finished': True, 'total_correct': 0, 'total_testcases': 97, 'runtime_percentile': None, 'status_memory': 'N/A', 'memory_percentile': None, 'pretty_lang': 'Python', 'submission_id': '1468064066', 'status_msg': 'Memory Limit Exceeded', 'state': 'SUCCESS'},

            "result_tle" : {'status_code': 14, 'lang': 'python', 'run_success': False, 'status_runtime': 'N/A', 'memory': 11952000, 'question_id': '409', 'elapsed_time': 11008, 'compare_result': '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', 'code_output': '', 'std_output': '', 'last_testcase': '"abccccdd"', 'expected_output': '7', 'task_finish_time': 1733121464193, 'task_name': 'judger.judgetask.Judge', 'finished': True, 'total_correct': 0, 'total_testcases': 97, 'runtime_percentile': None, 'status_memory': 'N/A', 'memory_percentile': None, 'pretty_lang': 'Python', 'submission_id': '1468065773', 'status_msg': 'Time Limit Exceeded', 'state': 'SUCCESS'},

            "result_ole" : {'status_code': 13, 'lang': 'python', 'run_success': False, 'status_runtime': 'N/A', 'memory': 12256000, 'question_id': '200', 'elapsed_time': 947, 'compare_result': '0000000000000000000000000000000000000000000000000', 'code_output': '', 'std_output': 'This will cause Output Limit Exceeded on LeetCode.\nThis will cause Output Limit Exceeded on LeetCode. 11484336 more chars', 'last_testcase': '[["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]', 'expected_output': '1', 'task_finish_time': 1733245589159, 'task_name': 'judger.judgetask.Judge', 'finished': True, 'total_correct': 0, 'total_testcases': 49, 'runtime_percentile': None, 'status_memory': 'N/A', 'memory_percentile': None, 'pretty_lang': 'Python', 'submission_id': '1469436577', 'status_msg': 'Output Limit Exceeded', 'state': 'SUCCESS'},

            "result_runtime_error" : {'status_code': 15, 'lang': 'python', 'run_success': False, 'runtime_error': 'Line 4: SyntaxError: invalid syntax', 'full_runtime_error': 'SyntaxError: invalid syntax\n               ^\n    syntax error\nLine 4  (Solution.py)', 'status_runtime': 'N/A', 'memory': 6508000, 'question_id': '409', 'elapsed_time': 21, 'compare_result': '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', 'code_output': '', 'std_output': '', 'last_testcase': '"abccccdd"', 'expected_output': '7', 'task_finish_time': 1733121520464, 'task_name': 'judger.judgetask.Judge', 'finished': True, 'total_correct': 0, 'total_testcases': 97, 'runtime_percentile': None, 'status_memory': 'N/A', 'memory_percentile': None, 'pretty_lang': 'Python', 'submission_id': '1468066640', 'status_msg': 'Runtime Error', 'state': 'SUCCESS'},

            "result_compile_error" : {'status_code': 20, 'lang': 'cpp', 'run_success': False, 'compile_error': "Line 6: Char 28: error: expected ';' after expression", 'full_compile_error': 'Line 6: Char 28: error: expected \';\' after expression\n    6 |     cout << "Hello, World!"  // Missing semicolon here\n      |                            ^\n      |                            ;', 'status_runtime': 'N/A', 'memory': 0, 'question_id': '409', 'task_finish_time': 1733121853942, 'task_name': 'judger.judgetask.Judge', 'finished': True, 'total_correct': None, 'total_testcases': None, 'runtime_percentile': None, 'status_memory': 'N/A', 'memory_percentile': None, 'pretty_lang': 'C++', 'submission_id': '1468070650', 'status_msg': 'Compile Error', 'state': 'SUCCESS'}

        }

        for result_name, result in results_possible.items():
            click.echo("\n\n")
            click.echo(result)
            click.echo("\n\n")
            if result:
                formatted_result = get_formatted_submission(result)
                click.echo(formatted_result)

                click.echo("\n\n")

    test_every_submission_parse()
                


def main():
    configure_logging()
    cli()
