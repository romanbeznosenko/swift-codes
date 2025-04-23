from custom_exceptions.SwiftParserError import SwiftParserError


class InvalidFileExtensionError(SwiftParserError):
    """Exception raised when a file does not have the required file extension."""

    def __init__(self):
        super().__init__("Invalid file extension: Expected '.csv' file.")
