class FetchingError(Exception):
    """Raised when there is an error fetching data from the external source."""

    pass


class ParsingError(Exception):
    """Raised when there is an error parsing the fetched data into the desired models."""

    pass


class FormattingError(Exception):
    """Raised when there is an error formatting the parsed data for output."""

    pass


class SubmissionError(Exception):
    """Raised when there is an error during submission or related actions."""

    pass


class ThemeError(Exception):
    """Raised when there is an error related to theme loading or validation."""

    pass


class ConfigError(Exception):
    """Raised when configuration is missing, invalid, or otherwise incorrect."""

    pass


class ProblemError(Exception):
    """Custom exception for problem-related errors."""

    pass


class CodeError(Exception):
    """Custom exception for code-related errors."""

    pass


class ProblemSetError(Exception):
    """Custom exception for problemset-related errors."""

    pass


class StatsError(Exception):
    """Custom exception for stats-related errors."""

    pass
