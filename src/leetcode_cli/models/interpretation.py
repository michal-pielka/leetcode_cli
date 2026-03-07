from dataclasses import dataclass


@dataclass
class InterpretationResult:
    status_code: int
    lang: str
    run_success: bool
    runtime_error: str | None
    full_runtime_error: str | None
    compile_error: str | None
    full_compile_error: str | None
    status_runtime: str
    memory: int
    display_runtime: str
    code_answer: list[str]
    code_output: list[str]
    std_output_list: list[str]
    elapsed_time: int | None
    task_finish_time: int | None
    task_name: str | None
    expected_status_code: int | None
    expected_lang: str | None
    expected_run_success: bool | None
    expected_status_runtime: str | None
    expected_memory: int | None
    expected_display_runtime: str | None
    expected_code_answer: list[str] | None
    expected_code_output: list[str] | None
    expected_std_output_list: list[str] | None
    expected_elapsed_time: int | None
    expected_task_finish_time: int | None
    expected_task_name: str | None
    correct_answer: bool | None
    compare_result: str | None
    total_correct: int | None
    total_testcases: int | None
    runtime_percentile: float | None
    status_memory: str | None
    memory_percentile: float | None
    pretty_lang: str | None
    submission_id: str | None
    status_msg: str
    state: str
