from custom_exceptions.SwiftParserError import SwiftParserError


class InvalidStringInputError(SwiftParserError):
    """Exception raised when a required string parameter is None, empty, or not a string."""

    def __init__(self):
        super().__init__("Invalid string input. Passed value is None, not a string or an empty string")
