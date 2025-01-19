from dataclasses import dataclass, field
from typing import Dict


@dataclass
class UserStatsModel:
    """
    Represents user stats by difficulty, including accepted, failed, untouched counts,
    plus how many users you beat per difficulty.
    """

    accepted: Dict[str, int]
    failed: Dict[str, int]
    untouched: Dict[str, int]
    beats: Dict[str, float] = field(default_factory=dict)  # e.g. {"EASY": 72.5, ...}
    total_submissions: int = 0


@dataclass
class UserActivityModel:
    """
    Represents daily submission activity for a user, typically covering the past year.
    The activity is a dict with timestamps as keys and submission counts as values.
    """

    daily_activity: Dict[int, int]
