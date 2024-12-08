from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class Problem:
    title: str
    question_frontend_id: str
    description: str
    examples: List[Dict[str, str]]
    constraints: List[str]
    category_title: str
    difficulty: str
    topic_tags: List[str]
    stats: Dict[str, str]
    likes: int = 0
    dislikes: int = 0
    is_paid_only: bool = False
    solution_info: Optional[Dict] = None
    code_snippets: List[Dict[str, str]] = field(default_factory=list)
