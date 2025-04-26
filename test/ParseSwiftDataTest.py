import unittest
from app.core.parser import parse_swift_data
import pandas as pd

from custom_exceptions.InvalidStringInputError import InvalidStringInputError
from custom_exceptions.FileNotFoundError import FileNotFoundError
from custom_exceptions.InvalidFileExtensionError import InvalidFileExtensionError
from custom_exceptions.MissingColumnError import MissingColumnError
from custom_exceptions.InvalidSwiftCodeError import InvalidSwiftCodeError
from custom_exceptions.DuplicateSwiftCodeError import DuplicateSwiftCodeError


class ParseSwiftDataTest(unittest.TestCase):
    """
    Unit test class for the function parse_swift_data. This class verifies that the function
    correctly parses SWIFT code data from CSV files, handles various edge cases, validates
    input parameters, and processes SWIFT codes according to specification.
    """

    def test_no_argument_passed(self):
        """
        Test case: No argument passed to the parse_swift_data function.
        Expected behavior: A TypeError is raised as the function requires a file path argument.
        """
        with self.assertRaises(TypeError):
            parse_swift_data()

    def test_none_argument_passed(self):
        """
        Test case: None is passed as an argument to the parse_swift_data function.
        Expected behavior: An InvalidStringInputError is raised because None is not a valid file path.
        """
        with self.assertRaises(InvalidStringInputError):
            parse_swift_data(None)

    def test_not_string_argument_1(self):
        """
        Test case: An integer is passed as an argument to the parse_swift_data function.
        Expected behavior: An InvalidStringInputError is raised because only strings are valid file paths.
        """
        with self.assertRaises(InvalidStringInputError):
            parse_swift_data(1)

    def test_not_string_argument_2(self):
        """
        Test case: A float is passed as an argument to the parse_swift_data function.
        Expected behavior: An InvalidStringInputError is raised because only strings are valid file paths.
        """
        with self.assertRaises(InvalidStringInputError):
            parse_swift_data(1.0)

    def test_not_string_argument_3(self):
        """
        Test case: A list is passed as an argument to the parse_swift_data function.
        Expected behavior: An InvalidStringInputError is raised because only strings are valid file paths.
        """
        with self.assertRaises(InvalidStringInputError):
            parse_swift_data([])

    def test_not_string_argument_4(self):
        """
        Test case: A dictionary is passed as an argument to the parse_swift_data function.
        Expected behavior: An InvalidStringInputError is raised because only strings are valid file paths.
        """
        with self.assertRaises(InvalidStringInputError):
            parse_swift_data({})

    def test_not_string_argument_5(self):
        """
        Test case: A tuple is passed as an argument to the parse_swift_data function.
        Expected behavior: An InvalidStringInputError is raised because only strings are valid file paths.
        """
        with self.assertRaises(InvalidStringInputError):
            parse_swift_data(())

    def test_not_file_name_1(self):
        """
        Test case: A non-existent file name is passed to the parse_swift_data function.
        Expected behavior: A FileNotFoundError is raised because the file does not exist.
        """
        with self.assertRaises(FileNotFoundError):
            parse_swift_data("Test")

    def test_not_file_name_2(self):
        """
        Test case: A directory name is passed instead of a file name to the parse_swift_data function.
        Expected behavior: A FileNotFoundError is raised because a directory is not a valid file.
        """
        with self.assertRaises(FileNotFoundError):
            parse_swift_data("src")

    def test_file_not_csv_1(self):
        """
        Test case: A text file (.txt) is passed to the parse_swift_data function.
        Expected behavior: An InvalidFileExtensionError is raised because only CSV files are supported.
        """
        with self.assertRaises(InvalidFileExtensionError):
            parse_swift_data("test/data/testFile.txt")

    def test_file_not_csv_2(self):
        """
        Test case: A file without extension is passed to the parse_swift_data function.
        Expected behavior: An InvalidFileExtensionError is raised because only CSV files are supported.
        """
        with self.assertRaises(InvalidFileExtensionError):
            parse_swift_data("test/data/testFileWithPermission")

    def test_incorrect_file_1(self):
        """
        Test case: An empty CSV file is passed to the parse_swift_data function.
        Expected behavior: A pandas.errors.EmptyDataError is raised because the file has no data.
        """
        with self.assertRaises(pd.errors.EmptyDataError):
            parse_swift_data("test/data/test_1.csv")

    def test_incorrect_file_2(self):
        """
        Test case: A CSV file missing required columns is passed to the parse_swift_data function.
        Expected behavior: A MissingColumnError is raised because the file does not contain all required columns.
        """
        with self.assertRaises(MissingColumnError):
            parse_swift_data("test/data/test_2.csv")

    def test_incorrect_file_3(self):
        """
        Test case: Another CSV file missing required columns is passed to the parse_swift_data function.
        Expected behavior: A MissingColumnError is raised because the file does not contain all required columns.
        """
        with self.assertRaises(MissingColumnError):
            parse_swift_data("test/data/test_3.csv")

    def test_invalid_swift_code_1(self):
        """
        Test case: A CSV file containing invalid SWIFT codes is passed to the parse_swift_data function.
        Expected behavior: An InvalidSwiftCodeError is raised because the file contains SWIFT codes that do not meet the required format.
        """
        with self.assertRaises(InvalidSwiftCodeError):
            parse_swift_data("test/data/test_8.csv")

    def test_invalid_swift_code_2(self):
        """
        Test case: A CSV file containing invalid SWIFT codes is passed to the parse_swift_data function.
        Expected behavior: An InvalidSwiftCodeError is raised because the file contains SWIFT codes that do not meet the required format.
        """
        with self.assertRaises(InvalidSwiftCodeError):
            parse_swift_data("test/data/test_9.csv")

    def test_invalid_swift_code_3(self):
        """
        Test case: A CSV file containing invalid SWIFT codes is passed to the parse_swift_data function.
        Expected behavior: An InvalidSwiftCodeError is raised because the file contains SWIFT codes that do not meet the required format.
        """
        with self.assertRaises(InvalidSwiftCodeError):
            parse_swift_data("test/data/test_10.csv")

    def test_invalid_swift_code_4(self):
        """
        Test case: A CSV file containing invalid SWIFT codes is passed to the parse_swift_data function.
        Expected behavior: An InvalidSwiftCodeError is raised because the file contains SWIFT codes that do not meet the required format.
        """
        with self.assertRaises(InvalidSwiftCodeError):
            parse_swift_data("test/data/test_11.csv")

    def test_valid_dataset_1(self):
        """
        Test case: A valid CSV file with a single SWIFT code is passed to the parse_swift_data function.
        Expected behavior: The function correctly parses the file and returns a list of dictionaries with the expected data.
        """
        result = parse_swift_data("test/data/test_5.csv")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['swift_code'], "AAISALTRXXX")
        self.assertEqual(result[0]['country_ISO2'], "AL")
        self.assertEqual(result[0]['country_name'], "ALBANIA")
        self.assertEqual(result[0]['bank_name'], "UNITED BANK OF ALBANIA SH.A")
        self.assertEqual(result[0]['is_headquarter'], True)

    def test_valid_dataset_2(self):
        """
        Test case: A valid CSV file with a single SWIFT code is passed to the parse_swift_data function.
        Expected behavior: The function correctly parses the file and returns a list of dictionaries with the expected data.
        """
        result = parse_swift_data("test/data/test_6.csv")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['swift_code'], "ABIEBGS1XXX")
        self.assertEqual(result[0]['country_ISO2'], "BG")
        self.assertEqual(result[0]['country_name'], "BULGARIA")
        self.assertEqual(result[0]['bank_name'], "ABV INVESTMENTS LTD")
        self.assertEqual(result[0]['is_headquarter'], True)

    def test_valid_dataset_3(self):
        """
        Test case: A valid CSV file with a headquarters and a branch SWIFT code is passed to the parse_swift_data function.
        Expected behavior: The function correctly parses the file and returns a list of dictionaries with the headquarters and branch properly identified.
        """
        result = parse_swift_data("test/data/test_7.csv")
        
        self.assertEqual(len(result), 2)
        
        # Verify headquarters data
        self.assertEqual(result[0]['swift_code'], "ABIEBGS1XXX")
        self.assertEqual(result[0]['country_ISO2'], "BG")
        self.assertEqual(result[0]['country_name'], "BULGARIA")
        self.assertEqual(result[0]['bank_name'], "ABV INVESTMENTS LTD")
        self.assertEqual(result[0]['is_headquarter'], True)

        # Verify branch data
        self.assertEqual(result[1]['swift_code'], "ABIEBGS1123")
        self.assertEqual(result[1]['country_ISO2'], "BG")
        self.assertEqual(result[1]['country_name'], "BULGARIA")
        self.assertEqual(result[1]['bank_name'], "")
        self.assertEqual(result[1]['is_headquarter'], False)

    def test_invalid_csv_file_1(self):
        """
        Test case: A CSV file with incorrect delimiter (semicolons instead of commas) is passed to the parse_swift_data function.
        Expected behavior: A MissingColumnError is raised because the file is parsed incorrectly due to the delimiter issue.
        """
        with self.assertRaises(MissingColumnError):
            parse_swift_data("test/data/test_12.csv")

    def test_duplicate_swift_code(self):
        """
        Test case: A CSV file with duplicate SWIFT codes is passed to the parse_swift_data function.
        Expected behavior: A DuplicateSwiftCodeError is raised because SWIFT codes must be unique.
        """
        with self.assertRaises(DuplicateSwiftCodeError):
            parse_swift_data("test/data/test_13.csv")

    def test_duplicate_swift_codes_2(self):
        """
        Test case: A CSV file with different SWIFT codes but same first 8 characters is passed to the parse_swift_data function.
        Expected behavior: The function correctly parses the file since the full SWIFT codes are different.
        """
        result = parse_swift_data("test/data/test_14.csv")

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['swift_code'], "ABIEBGS1123")
        self.assertEqual(result[1]['swift_code'], "ABIEBGS1122")
        
    def test_branch_ends_with_XXX(self):
        """
        Test case: A CSV file with a SWIFT code ending with XXX is passed to the parse_swift_data function.
        Expected behavior: The function correctly identifies it as a headquarters based on whether it ends with XXX.
        """
        result = parse_swift_data("test/data/test_15.csv")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['swift_code'], "ABIEBXXX")
        self.assertEqual(result[0]['is_headquarter'], False)

    def test_dataset_headers_only(self):
        """
        Test case: A CSV file with only headers and no data rows is passed to the parse_swift_data function.
        Expected behavior: The function returns an empty list.
        """
        result = parse_swift_data("test/data/test_16.csv")
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()