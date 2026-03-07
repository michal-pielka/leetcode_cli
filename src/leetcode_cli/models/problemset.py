from dataclasses import dataclass, field


@dataclass
class ProblemSummary:
    ac_rate: float
    difficulty: str
    question_id: str
    topic_tags: list[str]
    frontend_question_id: str
    paid_only: bool
    status: str | None
    title: str
    title_slug: str


@dataclass
class ProblemSet:
    total: int
    questions: list[ProblemSummary] = field(default_factory=list)
