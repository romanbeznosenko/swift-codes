import re


def is_valid_swift_code(code: str) -> bool:
    """
    Validates if a given string is a valid SWIFT/BIC code.

    SWIFT codes must follow these rules:
    - Must be either 8 or 11 characters long
    - First 4 characters: Bank code (letters only)
    - Characters 5-6: Country code (letters only)
    - Characters 7-8: Location code (letters and digits)
    - Characters 9-11: Branch code (optional, letters and digits)

    Args:
        code (str): The SWIFT/BIC code to validate

    Returns:
        bool: True if the code is a valid SWIFT/BIC code, False otherwise

    Examples:
        >>> is_valid_swift_code("AAAABBCC123")
        True
        >>> is_valid_swift_code("AABBCC")  # Too short
        False
        >>> is_valid_swift_code(123)  # Not a string
        False
    """

    if not isinstance(code, str):
        return False

    if not re.match(r'^[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?$', code):
        return False
    return True
