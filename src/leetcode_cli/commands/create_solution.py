import click
import logging

from leetcode_cli.managers.auth_service import AuthService
from leetcode_cli.managers.config_manager import ConfigManager
from leetcode_cli.managers.code_manager import CodeManager
from leetcode_cli.managers.problem_manager import ProblemManager
from leetcode_cli.managers.problemset_manager import ProblemSetManager
from leetcode_cli.exceptions.exceptions import ConfigError, CodeError, ProblemError

logger = logging.getLogger(__name__)


@click.command(short_help="Create a solution file for a LeetCode problem")
@click.argument("title_slug_or_id", required=False, metavar="TITLE_SLUG_OR_ID")
def create_cmd(title_slug_or_id):
    """
    Create a solution file for the specified LeetCode problem.

    Usage Examples: leetcode create, leetcode create .cpp, leetcode create two-sum.py, leetcode create 1.two-sum.py, leetcode create two-sum, leetcode create 1, leetcode create 1.cpp
    """
    try:
        config_manager = ConfigManager()
        auth_service = AuthService(config_manager)
        code_manager = CodeManager(config_manager)
        problemset_manager = ProblemSetManager(config_manager, auth_service)
        problem_manager = ProblemManager(
            config_manager, auth_service, problemset_manager
        )

        # If user doesn't provide an argument => use the chosen problem
        if not title_slug_or_id:
            title_slug_or_id = config_manager.get_chosen_problem()

            if not title_slug_or_id:
                click.echo(
                    "Error: No chosen problem found. Please specify a problem or use 'leetcode show' to select one."
                )
                return

        # Distinguish whether the user typed only an extension, e.g. ".cpp"
        if title_slug_or_id.startswith("."):
            # e.g. user typed `.cpp` => meaning extension=cpp, slug from config
            file_ext = title_slug_or_id
            title_slug = config_manager.get_chosen_problem()

            if not title_slug:
                click.echo(
                    "Error: No chosen problem found. Please specify or use 'leetcode show' to select one."
                )
                return

            try:
                frontend_id = problem_manager.get_problem_frontend_id(title_slug)
                # Let code_manager handle extension -> lang
                lang_slug, file_extension = code_manager.infer_lang_and_ext(
                    user_ext=file_ext
                )
                code_manager.create_solution_file_with_snippet(
                    frontend_id, title_slug, lang_slug, file_extension
                )
                click.echo(
                    f"Solution file '{frontend_id}.{title_slug}.{file_extension}' created successfully."
                )
                return

            except (ProblemError, CodeError) as e:
                click.echo(f"Error: {e}")
                return

        # Next, parse if there's a '.' in the argument => might be "123.py" or "1.two-sum.py", etc.
        parts = title_slug_or_id.split(".")
        is_id = title_slug_or_id.isdigit()

        # Cases:
        # 1) "1.two-sum.py" => [ "1", "two-sum", "py" ]
        # 2) "123.py"       => [ "123", "py" ]
        # 3) "two-sum.py"   => [ "two-sum", "py" ]
        # 4) "123"          => no dot
        # 5) "two-sum"      => no dot

        if "." in title_slug_or_id:
            if len(parts) == 3 and parts[0].isdigit():
                # e.g. "1.two-sum.py"
                frontend_id, title_slug, user_ext = parts[0], parts[1], parts[2]
                lang_slug, file_extension = code_manager.infer_lang_and_ext(
                    user_ext=user_ext
                )
                try:
                    code_manager.create_solution_file_with_snippet(
                        frontend_id, title_slug, lang_slug, file_extension
                    )
                    click.echo(
                        f"Solution file '{frontend_id}.{title_slug}.{file_extension}' created successfully."
                    )
                except (ProblemError, CodeError) as e:
                    click.echo(f"Error: {e}")

            elif len(parts) == 2 and parts[0].isdigit():
                # e.g. "123.py"
                frontend_id, user_ext = parts[0], parts[1]
                lang_slug, file_extension = code_manager.infer_lang_and_ext(
                    user_ext=user_ext
                )
                try:
                    title_slug = problem_manager.get_title_slug_for_frontend_id(
                        frontend_id
                    )
                    code_manager.create_solution_file_with_snippet(
                        frontend_id, title_slug, lang_slug, file_extension
                    )
                    click.echo(
                        f"Solution file '{frontend_id}.{title_slug}.{file_extension}' created successfully."
                    )
                except (ProblemError, CodeError) as e:
                    click.echo(f"Error: {e}")

            elif len(parts) == 2:
                # e.g. "two-sum.py"
                title_slug, user_ext = parts[0], parts[1]
                lang_slug, file_extension = code_manager.infer_lang_and_ext(
                    user_ext=user_ext
                )
                try:
                    frontend_id = problem_manager.get_problem_frontend_id(title_slug)
                    code_manager.create_solution_file_with_snippet(
                        frontend_id, title_slug, lang_slug, file_extension
                    )
                    click.echo(
                        f"Solution file '{frontend_id}.{title_slug}.{file_extension}' created successfully."
                    )
                except (ProblemError, CodeError) as e:
                    click.echo(f"Error: {e}")
            else:
                # e.g. "two.sum.py" => multiple dots => unknown format
                click.echo(
                    "Error: Unrecognized file format. Use e.g. 'two-sum.py' or '1.two-sum.py'."
                )
                return

        else:
            # no '.' => might be "123" or "two-sum"
            if is_id:
                # e.g. "123"
                frontend_id = title_slug_or_id
                try:
                    title_slug = problem_manager.get_title_slug_for_frontend_id(
                        frontend_id
                    )
                except ProblemError as e:
                    click.echo(f"Error: {e}")
                    return

                # fallback to config
                try:
                    lang_slug, file_extension = code_manager.infer_lang_and_ext()
                    code_manager.create_solution_file_with_snippet(
                        frontend_id, title_slug, lang_slug, file_extension
                    )
                    click.echo(
                        f"Solution file '{frontend_id}.{title_slug}.{file_extension}' created successfully."
                    )
                except (ProblemError, CodeError) as e:
                    click.echo(f"Error: {e}")

            else:
                # e.g. "two-sum"
                try:
                    # We only have the slug => retrieve the frontend ID from problem_manager
                    frontend_id = problem_manager.get_problem_frontend_id(
                        title_slug_or_id
                    )
                    lang_slug, file_extension = code_manager.infer_lang_and_ext()
                    code_manager.create_solution_file_with_snippet(
                        frontend_id, title_slug_or_id, lang_slug, file_extension
                    )
                    click.echo(
                        f"Solution file '{frontend_id}.{title_slug_or_id}.{file_extension}' created successfully."
                    )

                except (ProblemError, CodeError) as e:
                    click.echo(f"Error: {e}")

    except ConfigError as e:
        logger.error(e)
        click.echo(f"Configuration Error: {e}", err=True)

    except Exception as e:
        logger.exception("An unexpected error occurred during solution creation.")
        click.echo("An unexpected error occurred. Please try again.", err=True)
