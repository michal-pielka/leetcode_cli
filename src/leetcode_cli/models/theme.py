from dataclasses import dataclass, field


@dataclass
class ThemeData:
    """
    Holds all theme sub-dicts (ANSI_CODES, SYMBOLS, etc.).
    Each field corresponds to one key in the loaded theme data.
    """

    ANSI_CODES: dict[str, str] = field(default_factory=dict)
    SYMBOLS: dict[str, str] = field(default_factory=dict)
    INTERPRETATION: dict[str, dict[str, str]] = field(default_factory=dict)
    SUBMISSION: dict[str, dict[str, str]] = field(default_factory=dict)
    PROBLEMSET: dict[str, dict[str, str]] = field(default_factory=dict)
    PROBLEM_DESCRIPTION: dict[str, dict[str, str]] = field(default_factory=dict)
    STATS_FORMATTER: dict[str, dict[str, str]] = field(default_factory=dict)
