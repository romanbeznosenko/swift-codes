import re

def is_valid_swift_code(code: str) -> bool:
    if not isinstance(code, str):
        return False

    if not re.match(r'^[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?$', code):
        return False
    return True