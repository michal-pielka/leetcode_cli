# models/problemset.py
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class ProblemSummary:
    ac_rate: float
    difficulty: str
    question_id: str
    topic_tags: List[str]
    frontend_question_id: str
    paid_only: bool
    status: Optional[str]
    title: str
    title_slug: str

@dataclass
class ProblemSet:
    total: int
    questions: List[ProblemSummary] = field(default_factory=list)

