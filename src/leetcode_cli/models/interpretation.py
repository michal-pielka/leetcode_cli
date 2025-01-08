from dataclasses import dataclass
from typing import List, Optional


@dataclass
class InterpretationResult:
    status_code: int
    lang: str
    run_success: bool
    runtime_error: Optional[str]
    full_runtime_error: Optional[str]
    compile_error: Optional[str]
    full_compile_error: Optional[str]
    status_runtime: str
    memory: int
    display_runtime: str
    code_answer: List[str]
    code_output: List[str]
    std_output_list: List[str]
    elapsed_time: Optional[int]
    task_finish_time: Optional[int]
    task_name: Optional[str]
    expected_status_code: Optional[int]
    expected_lang: Optional[str]
    expected_run_success: Optional[bool]
    expected_status_runtime: Optional[str]
    expected_memory: Optional[int]
    expected_display_runtime: Optional[str]
    expected_code_answer: Optional[List[str]]
    expected_code_output: Optional[List[str]]
    expected_std_output_list: Optional[List[str]]
    expected_elapsed_time: Optional[int]
    expected_task_finish_time: Optional[int]
    expected_task_name: Optional[str]
    correct_answer: Optional[bool]
    compare_result: Optional[str]
    total_correct: Optional[int]
    total_testcases: Optional[int]
    runtime_percentile: Optional[float]
    status_memory: Optional[str]
    memory_percentile: Optional[float]
    pretty_lang: Optional[str]
    submission_id: Optional[str]
    status_msg: str
    state: str
