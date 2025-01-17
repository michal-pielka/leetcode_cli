import logging

from leetcode_cli.models.submission import SubmissionResult
from leetcode_cli.managers.theme_manager import ThemeManager
from leetcode_cli.exceptions.exceptions import ThemeError

logger = logging.getLogger(__name__)


class SubmissionFormatter:
    """
    Formats submission results using (ansi, symbol_left, symbol_right) theming.
    """

    def __init__(
        self, result: SubmissionResult, format_conf: dict, theme_manager: ThemeManager
    ):
        self.result = result
        self.format_conf = format_conf
        self.theme_manager = theme_manager
        self.theme_data = theme_manager.load_theme_data()

        self.ANSI_RESET = "\033[0m"  # Reset all styles

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

        runtime_error = getattr(self.result, "runtime_error", None)
        compile_error = getattr(self.result, "compile_error", None)
        full_runtime_error = getattr(self.result, "full_runtime_error", None)
        full_compile_error = getattr(self.result, "full_compile_error", None)

        # Obtain the styling for the overall status line
        try:
            ansi_code, symbol_left, symbol_right = self.theme_manager.get_styling(
                "SUBMISSION", "status_" + status_msg.lower().replace(" ", "_")
            )
        except ThemeError as te:
            raise te

        ansi_status = (
            f"{ansi_code}{symbol_left}{status_msg}{symbol_right}{self.ANSI_RESET}"
        )
        parsed_result = f"\n  {ansi_status} \n"

        # Now we call _format_label_value for each item, instead of manually building strings
        if show_language and lang:
            parsed_result += self._format_label_value("Language", lang)

        if show_testcases and total_correct is not None and total_testcases is not None:
            parsed_result += self._format_label_value(
                "Passed Testcases", f"{total_correct} / {total_testcases}"
            )

        if show_runtime_memory:
            # Runtime
            if time_ms and time_beats is not None:
                runtime_str = f"{time_ms} (Beats: {time_beats:.2f}%)"
                parsed_result += self._format_label_value("Runtime", runtime_str)

            # Memory
            if memory_size and memory_beats is not None:
                memory_str = f"{memory_size} (Beats: {memory_beats:.2f}%)"
                parsed_result += self._format_label_value("Memory Usage", memory_str)

        if last_testcase and show_testcases:
            parsed_result += self._format_label_value(
                "Failed Testcase", last_testcase.replace("\n", ", ")
            )

        if show_expected_output and expected_output:
            parsed_result += self._format_label_value(
                "Expected Output", expected_output
            )

        if show_code_output and code_output:
            code_output_str = (
                code_output if isinstance(code_output, str) else "\n".join(code_output)
            )
            parsed_result += self._format_label_value("Your Output", code_output_str)

        if show_stdout and std_output:
            std_output_str = (
                std_output if isinstance(std_output, str) else "\n".join(std_output)
            )
            parsed_result += self._format_label_value("Stdout", std_output_str)

        if show_errors:
            if runtime_error:
                parsed_result += self._format_label_value(
                    "Error Message", runtime_error
                )
            if compile_error:
                parsed_result += self._format_label_value(
                    "Error Message", compile_error
                )

        if detailed_errors:
            if full_runtime_error:
                parsed_result += self._format_label_value(
                    "Detailed Error", full_runtime_error
                )
            if full_compile_error:
                parsed_result += self._format_label_value(
                    "Detailed Error", full_compile_error
                )

        return parsed_result

    def _format_label_value(self, label: str, value: str) -> str:
        """
        Combines label and value on one line in a columnar style, using
        `_format_field_label` and `_format_field_value` under the hood.
        If the value has multiple lines, subsequent lines are padded.
        """
        # Build the label portion
        label_str = self._format_field_label(label)
        # Build the multi-line value portion
        value_lines = self._format_field_value(value).split("\n")

        if len(value_lines) == 1:
            # Single line scenario
            return f"  {label_str} {value_lines[0]}\n"

        # Multi-line scenario: the first line is next to label, subsequent lines are padded
        first_line = f"  {label_str} {value_lines[0]}\n"
        subsequent = ""
        # Indent subsequent lines so they align under the value column
        # "  " + 25 chars from label => 2 + 25 + 1 space => 28 total
        padding = " " * (2 + 25 + 1)
        for line in value_lines[1:]:
            if line.strip():
                subsequent += f"{padding}{line}\n"
            else:
                # If the line is empty, we can still add a newline to keep spacing consistent
                subsequent += f"{padding}\n"

        return first_line + subsequent

    def _format_field_label(self, label: str, width: int = 25) -> str:
        """
        Formats the field label using the 'field_label' mapping from SUBMISSION.
        """
        try:
            ansi_code, symbol_left, symbol_right = self.theme_manager.get_styling(
                "SUBMISSION", "label_field"
            )
        except ThemeError as te:
            logger.error(f"Theming Error: {te}")
            raise te

        # Combine label + symbol_right (often a colon) and left justify
        combined_label = f"{label}{symbol_right}"
        return f"{ansi_code}{symbol_left}{combined_label:<{width}}{self.ANSI_RESET}"

    def _format_field_value(self, value: str) -> str:
        """
        Formats the field value using the 'field_value' mapping from SUBMISSION.
        Handles multi-line values by splitting on newline.
        """
        try:
            ansi_code, symbol_left, symbol_right = self.theme_manager.get_styling(
                "SUBMISSION", "value_field"
            )
        except ThemeError as te:
            logger.error(f"Theming Error: {te}")
            raise te

        lines = value.split("\n")
        out_lines = []
        for line in lines:
            # Even if blank, we still produce a line
            out_lines.append(
                f"{ansi_code}{symbol_left}{line}{symbol_right}{self.ANSI_RESET}"
            )

        return "\n".join(out_lines)
