from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class FormattingConfig:
    """
    Represents the user's entire formatting configuration,
    including sub-sections: 'interpretation', 'submission', 'problem_show'.
    """

    interpretation: Dict[str, Any] = field(default_factory=dict)
    submission: Dict[str, Any] = field(default_factory=dict)
    problem_show: Dict[str, Any] = field(default_factory=dict)
