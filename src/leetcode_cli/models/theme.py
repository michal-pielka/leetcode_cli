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
    INTERPRETATION: Dict[str, Dict[str, str]] = field(default_factory=dict)
    SUBMISSION: Dict[str, Dict[str, str]] = field(default_factory=dict)
    PROBLEMSET: Dict[str, Dict[str, str]] = field(default_factory=dict)
    PROBLEM_DESCRIPTION: Dict[str, Dict[str, str]] = field(default_factory=dict)
    STATS_FORMATTER: Dict[str, Dict[str, str]] = field(default_factory=dict)
