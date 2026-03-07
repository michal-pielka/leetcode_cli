from dataclasses import dataclass, field
from typing import Any


@dataclass
class FormattingConfig:
    """
    Represents the user's entire formatting configuration,
    including sub-sections: 'interpretation', 'submission', 'problem_show'.
    """

    interpretation: dict[str, Any] = field(default_factory=dict)
    submission: dict[str, Any] = field(default_factory=dict)
    problem_show: dict[str, Any] = field(default_factory=dict)
