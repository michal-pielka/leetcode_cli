class FetchingError(Exception):
    """Raised when there is an error fetching data from the external source (e.g., network issues, invalid responses)."""
    pass

class ParsingError(Exception):
    """Raised when there is an error parsing the fetched data into the desired models."""
    pass

class FormattingError(Exception):
    """Raised when there is an error formatting the parsed data for output."""
    pass

class SubmissionError(Exception):
    """Raised when there is an error..."""
    pass

class ProblemSetFormatterError(Exception):
    """Custom exception for ProblemSetFormatter errors."""
    pass
