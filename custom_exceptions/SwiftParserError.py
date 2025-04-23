class SwiftParserError(Exception):
    """Base exception class for all SWIFT code parser related errors."""

    def __init__(self, message="An error occurred during SWIFT code parsing"):
        self.message = message
        super().__init__(self.message)
