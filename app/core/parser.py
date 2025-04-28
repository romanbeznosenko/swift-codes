import pandas as pd
from typing import List, Dict, Any
import os

from app.utils.validators import is_valid_swift_code

from custom_exceptions.MissingColumnError import MissingColumnError
from custom_exceptions.InvalidStringInputError import InvalidStringInputError
from custom_exceptions.FileNotFoundError import FileNotFoundError
from custom_exceptions.InvalidFileExtensionError import InvalidFileExtensionError
from custom_exceptions.InvalidSwiftCodeError import InvalidSwiftCodeError
from custom_exceptions.DuplicateSwiftCodeError import DuplicateSwiftCodeError


def parse_swift_data(file_path: str) -> List[Dict[str, Any]]:
    """
    Parse and validate SWIFT code data from a CSV file.

    This function reads a CSV file containing SWIFT code information,
    validates its structure and content, and transforms it into a standardized format.
    It applies business rules such as determining headquarter status based on the
    SWIFT code ending with 'XXX' and standardizing country codes to uppercase.

    Args:
        file_path (str): Path to the CSV file containing SWIFT code data.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each representing a SWIFT code entry
        with standardized field names and formatted values.

    Raises:
        InvalidStringInputError: If the file path is empty, not a string, or contains only whitespace.
        FileNotFoundError: If the file does not exist at the specified path.
        InvalidFileExtensionError: If the file is not a CSV file.
        pd.errors.ParserError: If the CSV file cannot be parsed due to formatting issues.
        pd.errors.EmptyDataError: If the CSV file is empty.
        MissingColumnError: If any required columns are missing from the CSV file.
        InvalidSwiftCodeError: If any SWIFT codes in the file are not valid.
        DuplicateSwiftCodeError: If the file contains duplicate SWIFT codes.
    """

    if not file_path or not isinstance(file_path, str) or not file_path.strip():
        raise InvalidStringInputError

    if not os.path.isfile(file_path):
        raise FileNotFoundError

    if not file_path.lower().endswith('.csv'):
        raise InvalidFileExtensionError

    try:
        df = pd.read_csv(file_path)
    except pd.errors.ParserError:
        raise pd.errors.ParserError
    except pd.errors.EmptyDataError:
        raise pd.errors.EmptyDataError

    needed_columns = [
        'SWIFT CODE',
        'COUNTRY ISO2 CODE',
        'COUNTRY NAME',
        'NAME',
        'ADDRESS',
    ]

    for column_name in needed_columns:
        if column_name not in df.columns:
            raise MissingColumnError(column_name)

    invalid_swift_code = df[~df['SWIFT CODE'].apply(is_valid_swift_code)]
    if not invalid_swift_code.empty:
        raise InvalidSwiftCodeError

    duplicate_swift_code_exists = df['SWIFT CODE'].duplicated().any()
    if duplicate_swift_code_exists:
        raise DuplicateSwiftCodeError

    df.columns = df.columns.str.strip()

    df = df.fillna('')

    df['COUNTRY NAME'] = df['COUNTRY NAME'].astype(str).str.upper().str.strip()
    df['COUNTRY ISO2 CODE'] = df['COUNTRY ISO2 CODE'].astype(
        str).str.upper().str.strip()
    df['ADDRESS'] = df['ADDRESS'].fillna(
        '').astype(str).str.upper().str.strip()
    df['NAME'] = df['NAME'].fillna('').astype(str).str.upper().str.strip()

    df['is_headquarter'] = (df['SWIFT CODE'].fillna('').astype(str).str.len() == 11) & \
        (df['SWIFT CODE'].fillna('').astype(str).str.endswith('XXX'))

    df = df.rename(columns={
        'SWIFT CODE': 'swift_code',
        'ADDRESS': 'address',
        'NAME': 'bank_name',
        'COUNTRY ISO2 CODE': 'country_ISO2',
        'COUNTRY NAME': 'country_name'
    })

    result_df = df[['swift_code', 'address', 'bank_name',
                    'country_ISO2', 'country_name', 'is_headquarter']]

    result = result_df.to_dict(orient="records")

    return result


if __name__ == "__main__":
    try:
        result = parse_swift_data(
            "./data/Interns_2025_SWIFT_CODES - Sheet1.csv")
        print(result)
    except Exception as e:
        print(e)
