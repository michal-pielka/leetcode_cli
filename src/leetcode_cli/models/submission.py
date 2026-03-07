from dataclasses import dataclass


@dataclass
class SubmissionResult:
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
    question_id: str | None
    elapsed_time: int | None
    compare_result: str | None
    code_output: str | None
    std_output: str | None
    last_testcase: str | None
    expected_output: str | None
    task_finish_time: int | None
    task_name: str | None
    finished: bool | None
    total_correct: int | None
    total_testcases: int | None
    runtime_percentile: float | None
    status_memory: str | None
    memory_percentile: float | None
    pretty_lang: str | None
    submission_id: str | None
    input_formatted: str | None
    input: str | None
    status_msg: str
    state: str
