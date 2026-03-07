from dataclasses import dataclass, field


@dataclass
class ThemeData:
    """
    Holds ANSI codes, symbols, and a flat styles dict.
    styles is keyed by section (status, difficulty, text, html, calendar, paid)
    then by key, each mapping to {"style": ..., "icon": ...}.
    """

    ANSI_CODES: dict[str, str] = field(default_factory=dict)
    SYMBOLS: dict[str, str] = field(default_factory=dict)
    styles: dict[str, dict[str, dict[str, str]]] = field(default_factory=dict)
