
# leetcode_cli/models/stats.py
from dataclasses import dataclass
from typing import Dict

@dataclass
class UserStatsModel:
    """
    Represents user stats by difficulty, including accepted, failed, and untouched counts.
    """
    accepted: Dict[str, int]
    failed: Dict[str, int]
    untouched: Dict[str, int]

@dataclass
class UserActivityModel:
    """
    Represents daily submission activity for a user, typically covering the past year.
    The activity is a dict with timestamps as keys and submission counts as values.
    """
    daily_activity: Dict[int, int]
