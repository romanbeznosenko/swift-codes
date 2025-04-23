from custom_exceptions.SwiftParserError import SwiftParserError


class FilePersmissionDeniedError(SwiftParserError):
    """Exception raised when a file exists but cannot be read due to permission restrictions."""

    def __init__(self):
        super().__init__("Permission denied: Unable to read the specified file.")
