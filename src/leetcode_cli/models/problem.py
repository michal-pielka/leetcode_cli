from dataclasses import dataclass, field


@dataclass
class Problem:
    title: str
    question_frontend_id: str
    description: str
    examples: list[dict[str, str]]
    constraints: list[str]
    category_title: str
    difficulty: str
    topic_tags: list[str]
    stats: dict[str, str]
    likes: int = 0
    dislikes: int = 0
    is_paid_only: bool = False
    solution_info: dict | None = None
    code_snippets: list[dict[str, str]] = field(default_factory=list)
