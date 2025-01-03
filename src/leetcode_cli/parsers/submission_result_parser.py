from typing import Dict, Any
from leetcode_cli.exceptions.exceptions import ParsingError
from leetcode_cli.models.submission import SubmissionResult

def parse_submission_result(json_data: Dict[str, Any]) -> SubmissionResult:
    # Define required fields
    required_fields = [
        "status_code",
        "status_msg",
        "lang",
        "run_success",
        "status_runtime",
        "memory",
        "state"
    ]

    # Validate required fields
    for field in required_fields:
        if field not in json_data:
            raise ParsingError(f"Missing required field '{field}' in submission result data.")

    """
    run_success = bool(json_data["run_success"])
    if not run_success:
        # If run was unsuccessful, at least one error field should be present
        error_fields = ["runtime_error", "compile_error"]
        if not any(json_data.get(error) for error in error_fields):
            raise ParsingError("Run failed but no error message provided in 'runtime_error' or 'compile_error'.")
    """

    return SubmissionResult(
        status_code=int(json_data["status_code"]),
        lang=str(json_data["lang"]),
        run_success=bool(json_data["run_success"]),
        runtime_error=json_data.get("runtime_error"),
        full_runtime_error=json_data.get("full_runtime_error"),
        compile_error=json_data.get("compile_error"),
        full_compile_error=json_data.get("full_compile_error"),
        status_runtime=str(json_data.get("status_runtime", "")),
        memory=int(json_data.get("memory", 0)),
        display_runtime=str(json_data.get("display_runtime", "")),
        question_id=json_data.get("question_id"),
        elapsed_time=json_data.get("elapsed_time"),
        compare_result=json_data.get("compare_result"),
        code_output=json_data.get("code_output"),
        std_output=json_data.get("std_output"),
        last_testcase=json_data.get("last_testcase"),
        expected_output=json_data.get("expected_output"),
        task_finish_time=json_data.get("task_finish_time"),
        task_name=json_data.get("task_name"),
        finished=json_data.get("finished"),
        total_correct=json_data.get("total_correct"),
        total_testcases=json_data.get("total_testcases"),
        runtime_percentile=json_data.get("runtime_percentile"),
        status_memory=json_data.get("status_memory"),
        memory_percentile=json_data.get("memory_percentile"),
        pretty_lang=json_data.get("pretty_lang"),
        submission_id=json_data.get("submission_id"),
        input_formatted=json_data.get("input_formatted"),
        input=json_data.get("input"),
        status_msg=str(json_data["status_msg"]),
        state=str(json_data["state"])
    )
