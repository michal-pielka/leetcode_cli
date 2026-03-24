import logging

from leetcode_cli.managers.theme_manager import ThemeManager
from leetcode_cli.models.interpretation import InterpretationResult

logger = logging.getLogger(__name__)


class InterpretationFormatter:
    """
    Formats 'run code' interpretation results per testcase.
    """

    def __init__(
        self,
        result: InterpretationResult,
        testcases_str: str,
        format_conf: dict,
        theme_manager: ThemeManager,
    ):
        self.result = result
        self.testcases_str = testcases_str
        self.format_conf = format_conf
        self.theme_manager = theme_manager
        self.theme_data = theme_manager.load_theme_data()

        self.ANSI_RESET = "" if theme_manager.raw_style else "\033[0m"

    def get_formatted_interpretation(self) -> str:
        status_code = self.result.status_code
        status_msg = self.result.status_msg
        lang = self.result.pretty_lang or self.result.lang
        total_testcases = self.result.total_testcases or 0

        show_language = self.format_conf.get("show_language", True)
        show_testcases = self.format_conf.get("show_testcases", True)
        show_expected_output = self.format_conf.get("show_expected_output", True)
        show_code_output = self.format_conf.get("show_code_output", True)
        show_stdout = self.format_conf.get("show_stdout", True)
        show_errors = self.format_conf.get("show_error_messages", True)
        detailed_errors = self.format_conf.get("show_detailed_error_messages", True)

        testcases_split = self.testcases_str.split("\n") if self.testcases_str else []
        parameters_in_testcase = len(testcases_split) // total_testcases if total_testcases > 0 else 1

        expected_outputs = self.result.expected_code_answer or []
        code_outputs = self.result.code_answer or []
        std_outputs = self.result.std_output_list or []

        runtime_error = self.result.runtime_error
        full_runtime_error = self.result.full_runtime_error
        compile_error = self.result.compile_error
        full_compile_error = self.result.full_compile_error

        parsed_result = ""

        if not expected_outputs:
            status_key = (status_msg or "Unknown").lower().replace(" ", "_")
            s_ansi, s_icon = self.theme_manager.get_styling("status", status_key)
            display_status = status_key.replace("_", " ").title()
            parsed_result += f"\n  {s_ansi}{s_icon} {display_status}{self.ANSI_RESET}\n"

            if show_language:
                parsed_result += self._format_label_value("Language", lang)

            if show_errors:
                if runtime_error:
                    parsed_result += self._format_label_value("Error Message", runtime_error)
                if compile_error:
                    parsed_result += self._format_label_value("Error Message", compile_error)

            if detailed_errors:
                if full_runtime_error:
                    parsed_result += self._format_label_value("Detailed Error", full_runtime_error)
                if full_compile_error:
                    parsed_result += self._format_label_value("Detailed Error", full_compile_error)

            return parsed_result

        for i, expected_out in enumerate(expected_outputs):
            if not expected_out:
                break

            start_idx = i * parameters_in_testcase
            end_idx = start_idx + parameters_in_testcase
            testcase_lines = testcases_split[start_idx:end_idx]

            code_out = code_outputs[i] if i < len(code_outputs) else None
            stdout_line = std_outputs[i] if i < len(std_outputs) else None

            if status_code == 10:
                status_key = "accepted" if code_out == expected_out else "wrong_answer"
            else:
                status_key = (status_msg or "Unknown").lower().replace(" ", "_")

            s_ansi, s_icon = self.theme_manager.get_styling("status", status_key)
            display_status = status_key.replace("_", " ").title()
            parsed_result += f"\n  {s_ansi}{s_icon} {display_status}{self.ANSI_RESET}\n"

            if show_language:
                parsed_result += self._format_label_value("Language", lang)

            if show_testcases and testcase_lines:
                parsed_result += self._format_label_value("Testcase", ", ".join(testcase_lines))

            if show_expected_output:
                parsed_result += self._format_label_value("Expected Output", expected_out)

            if show_code_output and code_out:
                parsed_result += self._format_label_value("Your Output", code_out)

            if show_stdout and stdout_line:
                parsed_result += self._format_label_value("Stdout", stdout_line)

            if show_errors:
                if runtime_error:
                    parsed_result += self._format_label_value("Error Message", runtime_error)
                if compile_error:
                    parsed_result += self._format_label_value("Error Message", compile_error)

            if detailed_errors:
                if full_runtime_error:
                    parsed_result += self._format_label_value("Detailed Error", full_runtime_error)
                if full_compile_error:
                    parsed_result += self._format_label_value("Detailed Error", full_compile_error)

        return parsed_result

    def _format_label_value(self, label: str, value: str) -> str:
        label_str = self._format_field_label(label)
        value_str = self._format_field_value(value)

        lines = value_str.split("\n")
        if len(lines) == 1:
            return f"  {label_str} {lines[0]}\n"

        first_line = f"  {label_str} {lines[0]}\n"
        padding = " " * (2 + 25 + 1)
        subsequent = ""
        for line in lines[1:]:
            if line.strip():
                subsequent += f"{padding}{line}\n"
        return first_line + subsequent

    def _format_field_label(self, label: str, width: int = 25) -> str:
        label_ansi, _ = self.theme_manager.get_styling("text", "label")
        combined_label = f"{label}:"
        return f"{label_ansi}{combined_label:<{width}}{self.ANSI_RESET}"

    def _format_field_value(self, value: str) -> str:
        value_ansi, _ = self.theme_manager.get_styling("text", "value")

        lines = value.split("\n")
        out_lines = []
        for line in lines:
            if not line.strip():
                out_lines.append("")
                continue
            out_lines.append(f"{value_ansi}{line}{self.ANSI_RESET}")
        return "\n".join(out_lines)
