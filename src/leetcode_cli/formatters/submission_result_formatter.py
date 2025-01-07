import logging

from leetcode_cli.graphics.ansi_codes import ANSI_RESET
from leetcode_cli.models.submission import SubmissionResult
from leetcode_cli.managers.theme_manager import ThemeManager
from leetcode_cli.exceptions.exceptions import ThemeError

logger = logging.getLogger(__name__)


class SubmissionFormatter:
    """
    Formats submission results using (ansi, symbol_left, symbol_right) theming.
    """
    def __init__(self, result: SubmissionResult, format_conf: dict, theme_manager: ThemeManager):
        self.result = result
        self.format_conf = format_conf
        self.theme_manager = theme_manager
        self.theme_data = theme_manager.load_theme_data()

    def get_formatted_submission(self) -> str:
        status_code = self.result.status_code
        status_msg = self.result.status_msg
        lang = self.result.pretty_lang or self.result.lang
        total_testcases = self.result.total_testcases

        show_language = self.format_conf.get("show_language", True)
        show_testcases = self.format_conf.get("show_testcases", True)
        show_runtime_memory = self.format_conf.get("show_runtime_memory", True)
        show_code_output = self.format_conf.get("show_code_output", True)
        show_stdout = self.format_conf.get("show_stdout", True)
        show_errors = self.format_conf.get("show_error_messages", True)
        detailed_errors = self.format_conf.get("show_detailed_error_messages", True)
        show_expected_output = self.format_conf.get("show_expected_output", True)

        time_ms = self.result.status_runtime
        time_beats = self.result.runtime_percentile
        memory_size = self.result.status_memory
        memory_beats = self.result.memory_percentile
        total_correct = self.result.total_correct
        total_testcases = self.result.total_testcases
        lang = self.result.pretty_lang or self.result.lang

        last_testcase = self.result.last_testcase
        expected_output = self.result.expected_output
        code_output = self.result.code_output
        std_output = self.result.std_output

        runtime_error = getattr(self.result, 'runtime_error', None)
        compile_error = getattr(self.result, 'compile_error', None)
        full_runtime_error = getattr(self.result, 'full_runtime_error', None)
        full_compile_error = getattr(self.result, 'full_compile_error', None)

        try:
            ansi_code, symbol_left, symbol_right = self.theme_manager.get_styling("SUBMISSION", status_msg)

        except ThemeError as te:
            raise te

        ansi_status = f"{ansi_code}{symbol_left}{status_msg}{symbol_right}{ANSI_RESET}"
        parsed_result = f"\n  {ansi_status} \n"

        # Format and append fields
        if show_language and lang:
            label = "Language"
            formatted_label = self._format_field_label(label)
            formatted_value = self._format_field_value(lang)
            parsed_result += f"  {formatted_label} {formatted_value}\n"

        if show_testcases and total_correct is not None and total_testcases is not None:
            label = "Passed Testcases"
            formatted_label = self._format_field_label(label)
            formatted_value = self._format_field_value(f'{total_correct} / {total_testcases}')
            parsed_result += f"  {formatted_label} {formatted_value}\n"

        if show_runtime_memory:
            if time_ms and time_beats is not None:
                formatted_time_beats = f"{time_beats:.2f}%"
                runtime_str = f'{time_ms} (Beats: {formatted_time_beats})'
                label = "Runtime"
                formatted_label = self._format_field_label(label)
                formatted_value = self._format_field_value(runtime_str)
                parsed_result += f"  {formatted_label} {formatted_value}\n"

            if memory_size and memory_beats is not None:
                formatted_memory_beats = f"{memory_beats:.2f}%"
                memory_str = f'{memory_size} (Beats: {formatted_memory_beats})'
                label = "Memory Usage"
                formatted_label = self._format_field_label(label)
                formatted_value = self._format_field_value(memory_str)
                parsed_result += f"  {formatted_label} {formatted_value}\n"

        if last_testcase and show_testcases:
            label = "Failed Testcase"
            formatted_label = self._format_field_label(label)
            formatted_value = self._format_field_value(last_testcase.replace("\n", ", "))
            parsed_result += f"  {formatted_label} {formatted_value}\n"

        if show_expected_output and expected_output:
            label = "Expected Output"
            formatted_label = self._format_field_label(label)
            formatted_value = self._format_field_value(expected_output)
            parsed_result += f"  {formatted_label} {formatted_value}\n"

        if show_code_output and code_output:
            code_output_str = code_output if isinstance(code_output, str) else "\n".join(code_output)
            label = "Your Output"
            formatted_label = self._format_field_label(label)
            formatted_value = self._format_field_value(code_output_str)
            parsed_result += f"  {formatted_label} {formatted_value}\n"

        if show_stdout and std_output:
            std_output_str = std_output if isinstance(std_output, str) else "\n".join(std_output)
            label = "Stdout"
            formatted_label = self._format_field_label(label)
            formatted_value = self._format_field_value(std_output_str)
            parsed_result += f"  {formatted_label} {formatted_value}\n"

        if show_errors:
            if runtime_error:
                label = "Error Message"
                formatted_label = self._format_field_label(label)
                formatted_value = self._format_field_value(runtime_error)
                parsed_result += f"  {formatted_label} {formatted_value}\n"

            if compile_error:
                label = "Error Message"
                formatted_label = self._format_field_label(label)
                formatted_value = self._format_field_value(compile_error)
                parsed_result += f"  {formatted_label} {formatted_value}\n"

        if detailed_errors:
            if full_runtime_error:
                label = "Detailed Error"
                formatted_label = self._format_field_label(label)
                formatted_value = self._format_field_value(full_runtime_error)
                parsed_result += f"  {formatted_label} {formatted_value}\n"

            if full_compile_error:
                label = "Detailed Error"
                formatted_label = self._format_field_label(label)
                formatted_value = self._format_field_value(full_compile_error)
                parsed_result += f"  {formatted_label} {formatted_value}\n"

        return parsed_result

    def _format_field_label(self, label: str, width: int = 25) -> str:
        """
        Formats the field label using the 'field_label' mapping.
        """
        try:
            ansi_code, symbol_left, symbol_right = self.theme_manager.get_styling("SUBMISSION", "field_label")

        except ThemeError as te:
            logger.error(f"Theming Error: {te}")
            raise te

        # Combine label and symbol_right (":") and left justify
        combined_label = f"{label}{symbol_right}"
        formatted_label = f"{ansi_code}{symbol_left}{combined_label:<{width}}{ANSI_RESET}"
        return formatted_label

    def _format_field_value(self, value: str) -> str:
        """
        Formats the field value using the 'field_value' mapping.
        """
        try:
            ansi_code, symbol_left, symbol_right = self.theme_manager.get_styling("SUBMISSION", "field_value")

        except ThemeError as te:
            logger.error(f"Theming Error: {te}")
            raise te

        formatted_value = f"{ansi_code}{symbol_left}{value}{symbol_right}{ANSI_RESET}"
        return formatted_value
