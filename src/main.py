import pandas as pd
from typing import Optional
import os
import re

from custom_exceptions.MissingColumnError import MissingColumnError
from custom_exceptions.InvalidStringInputError import InvalidStringInputError
from custom_exceptions.FileNotFoundError import FileNotFoundError
from custom_exceptions.FilePermissionDeniedError import FilePersmissionDeniedError
from custom_exceptions.InvalidFileExtensionError import InvalidFileExtensionError
from custom_exceptions.InvalidSwiftCodeError import InvalidSwiftCodeError


def is_valid_swift_code(code: str) -> bool:
    if not isinstance(code, str):
        return False

    if not re.match(r'^[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?$', code):
        return False
    return True


def parse_swift_data(file_path: str) -> Optional[pd.DataFrame]:
    if not file_path or not isinstance(file_path, str) or not file_path.strip():
        raise InvalidStringInputError

    if not os.path.isfile(file_path):
        raise FileNotFoundError

    if not os.access(file_path, os.R_OK):
        raise FilePersmissionDeniedError

    if not file_path.lower().endswith('.csv'):
        raise InvalidFileExtensionError

    try:
        df = pd.read_csv(file_path)
    except pd.errors.ParserError:
        raise pd.errors.ParserError

    needed_columns = [
        'SWIFT CODE',
        'COUNTRY ISO2 CODE',
        'COUNTRY NAME',
        'NAME',
        'ADDRESS',
        'TOWN NAME',
    ]

    for column_name in needed_columns:
        if column_name not in df.columns:
            raise MissingColumnError(column_name)

    invalid_swift_code = df[~df['SWIFT CODE'].apply(is_valid_swift_code)]
    if not invalid_swift_code.empty:
        raise InvalidSwiftCodeError

    df.columns = df.columns.str.strip()

    df['COUNTRY NAME'] = df['COUNTRY NAME'].fillna('').astype(str).str.upper()
    df['COUNTRY ISO2 CODE'] = df['COUNTRY ISO2 CODE'].fillna(
        '').astype(str).str.upper()

    df = df[needed_columns]

    df['IS_HEADQUARTERS'] = df['SWIFT CODE'].fillna(
        '').astype(str).str.endswith('XXX')
    df['SWIFT BASE'] = df['SWIFT CODE'].str[:8]

    headquarter_set = set(df[df['IS_HEADQUARTERS']]['SWIFT BASE'])

    def classify(code: str) -> str:
        is_headquarter = code.endswith('XXX')
        base = code[:8]
        is_branch = base in headquarter_set
        if is_headquarter and is_branch:
            return 'BOTH'
        elif is_headquarter:
            return 'HEADQUARTERS'
        elif is_branch:
            return 'BRANCH'
        else:
            return 'UNKNOWN'

    df['TYPE'] = df['SWIFT CODE'].apply(classify)

    headquarter_map = df[df['IS_HEADQUARTERS']].set_index('SWIFT BASE')[
        'SWIFT CODE'].to_dict()
    df['HEADQUARTER_SWIFT_CODE'] = df['SWIFT BASE'].map(headquarter_map)

    df = df.drop(columns=['IS_HEADQUARTERS', 'SWIFT BASE'])

    return df


if __name__ == "__main__":
    try:
        df = parse_swift_data("./data/Interns_2025_SWIFT_CODES - Sheet1.csv")
        print(df.head)
    except Exception as e:
        print(e)
