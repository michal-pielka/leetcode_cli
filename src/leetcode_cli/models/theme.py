from dataclasses import dataclass, field
from typing import Dict

@dataclass
class ThemeData:
    """
    Holds all theme data loaded from the theme files:
    - ANSI_CODES
    - SYMBOLS
    - MAPPINGS
    Each category in MAPPINGS is a dict of items => {ansi: str, symbol: str}.
    """
    ANSI_CODES: Dict[str, str] = field(default_factory=dict)
    SYMBOLS: Dict[str, str] = field(default_factory=dict)
    MAPPINGS: Dict[str, Dict[str, Dict[str, str]]] = field(default_factory=dict)
