from custom_exceptions.SwiftParserError import SwiftParserError


class InvalidSwiftCodeError(SwiftParserError):
    """Exception raised when the dataset contains one or more invalid SWIFT codes."""

    def __init__(self):
        super().__init__("Invalid SWIFT codes found in the dataset.")
