from custom_exceptions.SwiftParserError import SwiftParserError


class MissingColumnError(SwiftParserError):
    """Exception raised when the dataset does not contain one or more expected columns."""

    def __init__(self, column_name):
        super().__init__(f"Missing required column: {column_name}")
