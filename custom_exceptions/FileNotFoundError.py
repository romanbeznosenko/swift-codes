from custom_exceptions.SwiftParserError import SwiftParserError


class FileNotFoundError(SwiftParserError):
    """Exception raised when a specified file path does not exist or is not a file."""

    def __init__(self):
        super().__init__("The specified file does not exist or is not a regular file.")
