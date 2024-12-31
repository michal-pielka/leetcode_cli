from dataclasses import dataclass, field
from typing import Dict

@dataclass
class ThemeData:
    """
    Holds all theme sub-dicts (ANSI_CODES, SYMBOLS, etc.).
    Each field corresponds to one key in the loaded theme data.
    """
    ANSI_CODES: Dict[str, str] = field(default_factory=dict)
    SYMBOLS: Dict[str, str] = field(default_factory=dict)

    INTERPRETATION_ANSI_CODES: Dict[str, str] = field(default_factory=dict)
    INTERPRETATION_SYMBOLS: Dict[str, str] = field(default_factory=dict)

    PROBLEMSET_FORMATTER_ANSI_CODES: Dict[str, str] = field(default_factory=dict)
    PROBLEMSET_FORMATTER_SYMBOLS: Dict[str, str] = field(default_factory=dict)

    SUBMISSION_ANSI_CODES: Dict[str, str] = field(default_factory=dict)
    SUBMISSION_SYMBOLS: Dict[str, str] = field(default_factory=dict)

    PROBLEM_FORMATTER_ANSI_CODES: Dict[str, str] = field(default_factory=dict)
    PROBLEM_FORMATTER_SYMBOLS: Dict[str, str] = field(default_factory=dict)

    STATS_FORMATTER_DIFFICULTY_COLORS: Dict[str, str] = field(default_factory=dict)
    STATS_FORMATTER_SYMBOLS: Dict[str, str] = field(default_factory=dict)
