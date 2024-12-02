import click
import json
import logging
import os
from datetime import datetime

from .parsers.submission_parser import get_formatted_submission, SubmissionParseError
from .parsers.problem_parser import LeetCodeProblemParser
from .parsers.problemset_parser import LeetCodeProblemsetParser
from .parsers.stats_parser import get_formatted_leetcode_stats, get_formatted_daily_activity

from .user_utils import get_problem_by_key_value, set_chosen_problem, get_chosen_problem
from .user_utils import get_cookie, get_username, get_language, extract_csrf_token, set_cookie, set_username, set_language

from .data_fetching.stats_fetcher import fetch_user_stats, fetch_user_activity
from .data_fetching.problem_fetcher import fetch_problem_data
from .data_fetching.problemset_fetcher import fetch_problemset

from .leetcode_problem.problem_submitter import submit_and_get_result, SubmissionError
from .leetcode_problem.solution_file_creator import create_solution_file

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logging.disable(logging.CRITICAL)

# Define context settings for click to adjust help message formatting
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'], max_content_width=200)

possible_lang_slugs = ["cpp", "java", "python", "python3", "c", "csharp", "javascript", "typescript", "php", "swift", "kotlin", "dart", "golang", "ruby", "scala", "rust", "racket", "erlang", "elixir"]
possible_file_extensions = ["cpp", "java", "py", "py3", "c", "cs", "js", "ts", "php", "swift", "kt", "dart", "go", "rb", "scala", "rs", "rkt", "erl", "ex"]

extension_to_lang_slug = {
    possible_file_extensions[i] : possible_lang_slugs[i] for i in range(len(possible_lang_slugs))
}

lang_slug_to_extension = {
    possible_lang_slugs[i] : possible_file_extensions[i] for i in range(len(possible_file_extensions))
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
        if not lang_slug or lang_slug.lower() not in possible_lang_slugs:
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


def resolve_title_slug(title_slug_or_id):
    if title_slug_or_id.isdigit():
        # Fetch title_slug from problems metadata using question ID
        problem = get_problem_by_key_value('frontendQuestionId', title_slug_or_id)
        if not problem:
            click.echo(f"Error: Problem with ID '{title_slug_or_id}' not found in cached data. Please run 'leetcode download_problems' to update the cache.")
            return None
        return problem['titleSlug']
    else:
        return title_slug_or_id









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
            if value not in possible_lang_slugs:
                click.echo("Incorrect language, choose from these:")
                for lang in possible_lang_slugs:
                    click.echo(f"  {lang}")
                return
            set_language(value)
            logger.info(f"Preferred language set to '{value}'.")
            click.echo(f"Preferred language set to '{value}'.")
    except Exception as e:
        logger.error(f"Failed to set {key}: {e}")
        click.echo(f"Error: Failed to set {key}. {e}")

@cli.command(short_help='List problems')
@click.option(
    '--difficulty',
    type=click.Choice(['all', 'Easy', 'Medium', 'Hard'], case_sensitive=False),
    default='all',  # Set default to 'all'
    show_default=True,
    help='Filter by difficulty (default: all)'
)
@click.option(
    '--tags',
    multiple=True,
    default=(),  # Use an empty tuple as the default for multiple=True
    show_default='all',
    help='Filter by tags (default: all)'
)
@click.option(
    '--limit',
    type=int,
    default=50,
    show_default=True,
    help='Limit the number of results'
)
@click.option(
    '--page',
    type=int,
    default=1,
    show_default=True,
    help='Display a specific page'
)
def list(difficulty, tags, limit, page):
    """List LeetCode problems with optional filters."""
    logger.debug("Starting 'list' command with parameters:")
    logger.debug(f"Difficulty: '{difficulty}'")
    logger.debug(f"Tags: {tags}")
    logger.debug(f"Limit: {limit}")
    logger.debug(f"Page: {page}")

    if difficulty == "all":
        difficulty = None
    else:
        difficulty = difficulty.upper()

    if tags == "all":
        tags = None

    try:
        skip = (page - 1) * limit
        category_slug = "all-code-essentials"

        tags_list = list(tags) if tags else []

        # Fetch cookie and CSRF token
        cookie = get_cookie()
        csrf_token = extract_csrf_token(cookie) if cookie else None

        # Fetch problemset
        problems_dict = fetch_problemset(
            cookie=cookie,
            csrf_token=csrf_token,
            tags=tags_list,
            difficulty=difficulty,
            limit=limit,
            skip=skip,
            category_slug=category_slug
        )

        logger.debug(f"Fetched Problems: {problems_dict}")

        if not problems_dict:
            click.echo("Error: Failed to fetch problem list.")
            return

        parser = LeetCodeProblemsetParser(problems_dict)
        formatted_problems = parser.get_formatted_questions()
        click.echo()
        click.echo(formatted_problems)
        click.echo()


    except Exception as e:
        logger.error(f"An error occurred while listing problems: {e}", exc_info=True)
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
        problem_data = {}

        if title_slug_or_id.isdigit():
            problem_data = get_problem_by_key_value('frontendQuestionId', title_slug_or_id)

            if not problem_data:
                click.echo(f"Error: In order to fetch problem data by questionID, you need to download problems' metadata: leetcode download-problems")
                return
        else:
            problem_data = get_problem_by_key_value('titleSlug', title_slug_or_id)


        title_slug = title_slug_or_id
        if problem_data:
            title_slug = problem_data['titleSlug']

        metadata = fetch_problem_data(title_slug)

        if not metadata or not metadata['data']['question']:
            click.echo(f"Error: Can't fetch problem: {title_slug_or_id}")
            return

        # Update the config file
        set_chosen_problem(title_slug)

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

        click.echo()
        for section in sections_to_display:
            if section in all_sections:
                content = all_sections[section]()
                if content:
                    click.echo(content)
                    click.echo()

    except Exception as e:
        logger.error(f"An error occurred while showing problem details: {e}", exc_info=True)
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
            stats_data = fetch_leetcode_user_stats(username)
            if stats_data:
                formatted_stats = get_formatted_leetcode_stats(stats_data)
                click.echo()
                click.echo(formatted_stats)
                click.echo()
            else:
                click.echo("Error: Failed to fetch stats data.")

        if 'calendar' in sections_to_include:
            current_year = datetime.utcnow().year
            previous_year = current_year - 1

            activity_current = fetch_leetcode_activity(username, current_year)
            activity_previous = fetch_leetcode_activity(username, previous_year)

            if activity_current and activity_previous:
                from .parsers.parser_utils.leetcode_stats_parser import join_and_slice_calendars, fill_daily_activity
                joined_activity = join_and_slice_calendars(activity_previous, activity_current)
                filled_activity = fill_daily_activity(joined_activity)
                formatted_activity = get_formatted_daily_activity(filled_activity)
                click.echo()
                click.echo(formatted_activity)
                click.echo()
            else:
                click.echo("Error: Failed to fetch activity data.")

    except Exception as e:
        logger.error(f"An error occurred while fetching stats: {e}")
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

                title_slug = resolve_title_slug(title_slug_part)
                if not title_slug:
                    return

            else:
                # **Usage:** leetcode create two-sum or leetcode create 1
                lang_slug, file_extension = get_language_and_extension()
                if not lang_slug:
                    return

                title_slug = resolve_title_slug(title_slug_or_id)
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


@cli.command(short_help='Submit a solution file')
@click.argument('file_path', required=True, type=click.Path(exists=True))
def submit(file_path):
    """
    Submit a solution file for a problem.

    Usage:
        leetcode submit 1.two-sum.py
    """
    try:
        # Verify the file exists
        if not os.path.isfile(file_path):
            click.echo(f"Error: The file '{file_path}' does not exist.")
            return

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
            click.echo()
            click.echo(formatted_result)
            click.echo()
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
        from .user_utils import get_problems_data_path
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



######################################
#     T       E        S        T    #
######################################





        #    parsers = {
        #        10: _format_accepted,
        #        11: _format_wrong_answer,
        #        12: _format_memory_limit_exceeded,
        #        13: _format_output_limit_exceeded,
        #        14: _format_time_limit_exceeded,
        #        15: _format_runtime_error,
        #        20: _format_compile_error,
        #     }




@cli.command(short_help="TEST SOME CODE // REMOVE LATER")
def test():
    def test_every_submission_parse():
        #result = submit_and_get_result(cookie, csrf_token, title_slug, question_id, file_path)
        results_possible = {
            "result_accepted" : {'status_code': 10, 'lang': 'python', 'run_success': True, 'status_runtime': '7 ms', 'memory': 12008000, 'display_runtime': '7', 'question_id': '409', 'elapsed_time': 46, 'compare_result': '1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111', 'code_output': '', 'std_output': '', 'last_testcase': '', 'expected_output': '', 'task_finish_time': 1733121005250, 'task_name': 'judger.judgetask.Judge', 'finished': True, 'total_correct': 97, 'total_testcases': 97, 'runtime_percentile': 17.433899999999994, 'status_memory': '12 MB', 'memory_percentile': 5.559299999999997, 'pretty_lang': 'Python', 'submission_id': '1468060198', 'status_msg': 'Accepted', 'state': 'SUCCESS'},

            "result_wrong" : {'status_code': 11, 'lang': 'python', 'run_success': True, 'status_runtime': 'N/A', 'memory': 12124000, 'display_runtime': '0', 'question_id': '409', 'elapsed_time': 33, 'compare_result': '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', 'code_output': '123', 'std_output': 'std line 1\nstd line 2\n', 'last_testcase': '"abccccdd"', 'expected_output': '7', 'task_finish_time': 1733121084175, 'task_name': 'judger.judgetask.Judge', 'finished': True, 'total_correct': 0, 'total_testcases': 97, 'runtime_percentile': None, 'status_memory': 'N/A', 'memory_percentile': None, 'pretty_lang': 'Python', 'submission_id': '1468061226', 'input_formatted': '"abccccdd"', 'input': '"abccccdd"', 'status_msg': 'Wrong Answer', 'state': 'SUCCESS'},

            "result_mle" : {'status_code': 12, 'lang': 'python', 'run_success': False, 'status_runtime': 'N/A', 'memory': 976576000, 'question_id': '409', 'elapsed_time': 399, 'compare_result': '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', 'code_output': '', 'std_output': '', 'last_testcase': '"abccccdd"', 'expected_output': '7', 'task_finish_time': 1733121307119, 'task_name': 'judger.judgetask.Judge', 'finished': True, 'total_correct': 0, 'total_testcases': 97, 'runtime_percentile': None, 'status_memory': 'N/A', 'memory_percentile': None, 'pretty_lang': 'Python', 'submission_id': '1468064066', 'status_msg': 'Memory Limit Exceeded', 'state': 'SUCCESS'},

            "result_tle" : {'status_code': 14, 'lang': 'python', 'run_success': False, 'status_runtime': 'N/A', 'memory': 11952000, 'question_id': '409', 'elapsed_time': 11008, 'compare_result': '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', 'code_output': '', 'std_output': '', 'last_testcase': '"abccccdd"', 'expected_output': '7', 'task_finish_time': 1733121464193, 'task_name': 'judger.judgetask.Judge', 'finished': True, 'total_correct': 0, 'total_testcases': 97, 'runtime_percentile': None, 'status_memory': 'N/A', 'memory_percentile': None, 'pretty_lang': 'Python', 'submission_id': '1468065773', 'status_msg': 'Time Limit Exceeded', 'state': 'SUCCESS'},


            "result_runtime_error" : {'status_code': 15, 'lang': 'python', 'run_success': False, 'runtime_error': 'Line 4: SyntaxError: invalid syntax', 'full_runtime_error': 'SyntaxError: invalid syntax\n               ^\n    syntax error\nLine 4  (Solution.py)', 'status_runtime': 'N/A', 'memory': 6508000, 'question_id': '409', 'elapsed_time': 21, 'compare_result': '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', 'code_output': '', 'std_output': '', 'last_testcase': '"abccccdd"', 'expected_output': '7', 'task_finish_time': 1733121520464, 'task_name': 'judger.judgetask.Judge', 'finished': True, 'total_correct': 0, 'total_testcases': 97, 'runtime_percentile': None, 'status_memory': 'N/A', 'memory_percentile': None, 'pretty_lang': 'Python', 'submission_id': '1468066640', 'status_msg': 'Runtime Error', 'state': 'SUCCESS'},

            "result_compile_error" : {'status_code': 20, 'lang': 'cpp', 'run_success': False, 'compile_error': "Line 6: Char 28: error: expected ';' after expression", 'full_compile_error': 'Line 6: Char 28: error: expected \';\' after expression\n    6 |     cout << "Hello, World!"  // Missing semicolon here\n      |                            ^\n      |                            ;', 'status_runtime': 'N/A', 'memory': 0, 'question_id': '409', 'task_finish_time': 1733121853942, 'task_name': 'judger.judgetask.Judge', 'finished': True, 'total_correct': None, 'total_testcases': None, 'runtime_percentile': None, 'status_memory': 'N/A', 'memory_percentile': None, 'pretty_lang': 'C++', 'submission_id': '1468070650', 'status_msg': 'Compile Error', 'state': 'SUCCESS'}

        }

        for result_name, result in results_possible.items():
            click.echo(result_name)
            if result:
                formatted_result = get_formatted_submission(result)
                click.echo(formatted_result)

                click.echo("\n\n")

    test_every_submission_parse()


if __name__ == '__main__':
    cli()
