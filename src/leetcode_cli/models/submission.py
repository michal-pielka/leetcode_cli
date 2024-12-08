from dataclasses import dataclass
from typing import Optional

@dataclass
class SubmissionResult:
    status_code: int
    lang: str
    run_success: bool
    status_runtime: str
    memory: int
    display_runtime: str
    question_id: Optional[str]
    elapsed_time: Optional[int]
    compare_result: Optional[str]
    code_output: Optional[str]
    std_output: Optional[str]
    last_testcase: Optional[str]
    expected_output: Optional[str]
    task_finish_time: Optional[int]
    task_name: Optional[str]
    finished: Optional[bool]
    total_correct: Optional[int]
    total_testcases: Optional[int]
    runtime_percentile: Optional[float]
    status_memory: Optional[str]
    memory_percentile: Optional[float]
    pretty_lang: Optional[str]
    submission_id: Optional[str]
    input_formatted: Optional[str]
    input: Optional[str]
    status_msg: str
    state: str
