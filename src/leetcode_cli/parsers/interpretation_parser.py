from typing import Dict, Any
from leetcode_cli.exceptions.exceptions import ParsingError
from leetcode_cli.models.interpretation import InterpretationResult

def parse_interpretation_result(json_data: Dict[str, Any]) -> InterpretationResult:
    # Validate required fields, at least status_code and status_msg
    required_fields = ["status_code", "status_msg", "lang", "run_success", "code_answer", "code_output", "std_output_list", "state"]
    for f in required_fields:
        if f not in json_data:
            raise ParsingError(f"Missing '{f}' in interpretation result data.")
    
    return InterpretationResult(
        status_code=int(json_data["status_code"]),
        lang=json_data["lang"],
        run_success=bool(json_data["run_success"]),
        status_runtime=json_data.get("status_runtime", ""),
        memory=json_data.get("memory", 0),
        display_runtime=json_data.get("display_runtime", ""),
        code_answer=json_data.get("code_answer", []),
        code_output=json_data.get("code_output", []),
        std_output_list=json_data.get("std_output_list", []),
        elapsed_time=json_data.get("elapsed_time"),
        task_finish_time=json_data.get("task_finish_time"),
        task_name=json_data.get("task_name"),
        expected_status_code=json_data.get("expected_status_code"),
        expected_lang=json_data.get("expected_lang"),
        expected_run_success=json_data.get("expected_run_success"),
        expected_status_runtime=json_data.get("expected_status_runtime"),
        expected_memory=json_data.get("expected_memory"),
        expected_display_runtime=json_data.get("expected_display_runtime"),
        expected_code_answer=json_data.get("expected_code_answer"),
        expected_code_output=json_data.get("expected_code_output"),
        expected_std_output_list=json_data.get("expected_std_output_list"),
        expected_elapsed_time=json_data.get("expected_elapsed_time"),
        expected_task_finish_time=json_data.get("expected_task_finish_time"),
        expected_task_name=json_data.get("expected_task_name"),
        correct_answer=json_data.get("correct_answer"),
        compare_result=json_data.get("compare_result"),
        total_correct=json_data.get("total_correct"),
        total_testcases=json_data.get("total_testcases"),
        runtime_percentile=json_data.get("runtime_percentile"),
        status_memory=json_data.get("status_memory"),
        memory_percentile=json_data.get("memory_percentile"),
        pretty_lang=json_data.get("pretty_lang"),
        submission_id=json_data.get("submission_id"),
        status_msg=json_data["status_msg"],
        state=json_data["state"]
    )
