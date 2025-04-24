from custom_exceptions.SwiftParserError import SwiftParserError

class DuplicateSwiftCodeError(SwiftParserError):
    def __init__(self, message="'SWIFT CODE' column values should be unique!"):
        super().__init__(message)