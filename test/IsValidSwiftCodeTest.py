import unittest
from app.utils.validators import is_valid_swift_code


class ISValidSwiftCodeTest(unittest.TestCase):
    """
    Unit test class for the function is_valid_swift_code. This class verifies that the function
    correctly identifies valid and invalid SWIFT codes, and handles various edge cases and input types
    """

    def test_no_argument_passed(self):
        """
        Test case: No argument passed to the is_valid_swift_code function.
        Expected behavior: A TypeError is raised as the function requires an argument.
        """
        with self.assertRaises(TypeError):
            is_valid_swift_code()

    def test_none_argument_passed(self):
        """
        Test case: None is passed as an argument to the is_valid_swift_code function.
        Expected behavior: The function should return False because None is not a valid argument.
        """
        result = is_valid_swift_code(None)
        self.assertFalse(result)

    def test_not_string_argument_passed_1(self):
        """
        Test case: An integer is passed as an argument to the is_valid_swift_code function.
        Expected behavior: The function should return False because only strings are valid SWIFT codes.
        """
        result = is_valid_swift_code(25)
        self.assertFalse(result)

    def test_not_string_argument_passed_2(self):
        """
        Test case: A list is passed as an argument to the is_valid_swift_code function.
        Expected behavior: The function should return False because only strings are valid SWIFT codes.
        """
        result = is_valid_swift_code([])
        self.assertFalse(result)

    def test_not_string_argument_passed_3(self):
        """
        Test case: A tuple is passed as an argument to the is_valid_swift_code function.
        Expected behavior: The function should return False because only strings are valid SWIFT codes.
        """
        result = is_valid_swift_code(())
        self.assertFalse(result)

    def test_not_string_argument_passed_4(self):
        """
        Test case: A dictionary is passed as an argument to the is_valid_swift_code function.
        Expected behavior: The function should return False because only strings are valid SWIFT codes.
        """
        result = is_valid_swift_code({})
        self.assertFalse(result)

    def test_empty_string_passed(self):
        """
        Test case: An empty string is passed as an argument to the is_valid_swift_code function.
        Expected bahvior: The function should return False because an empty string is not a valid SWIFT code.
        """
        result = is_valid_swift_code("")
        self.assertFalse(result)

    def test_invalid_code_1(self):
        """
        Test case: A SWIFT code with invalid characters is passed to the function.
        Example: "AAAA-BB-CC-123"
        Expected behavior: The function should return False because the code contains dashes which are not allowed.
        """
        result = is_valid_swift_code("AAAA-BB-CC-123")
        self.assertFalse(result)

    def test_invalid_code_2(self):
        """
        Test case: A SWIFT code that starts with numbers is passed to the function.
        Example: "1234BBCC123"
        Expected behavior: The function should return False because the code starts with numbers instead of letters.
        """
        result = is_valid_swift_code("1234BBCC123")
        self.assertFalse(result)

    def test_invalid_code_3(self):
        """
        Test case: An invalid SWIFT code is passed as an argument to the function.
        Example: "A1AABBCC123"
        Expected behavior: The function should return False because Bank code (characters 1-4) should contain letters from A to Z.
        """
        result = is_valid_swift_code("A1AABBCC123")
        self.assertFalse(result)

    def test_invalid_code_4(self):
        """
        Test case: An invalid SWIFT code is passed as an argument to the function.
        Example: "AAAA12CC123"
        Expected behavior: The function should return False because Country code (characters 5-6) should contain letters from A to Z. 
        """
        result = is_valid_swift_code("AAAA12CC123")
        self.assertFalse(result)

    def test_invalid_code_5(self):
        """
        Test case: An invalid SWIFT code is passed as an argument to the function.
        Example: "AAAAB2CC123"
        Expected behavior: The function should return False because Country code (characters 5-6) should contain letters from A to Z. 
        """
        result = is_valid_swift_code("AAAAB2CC123")
        self.assertFalse(result)

    def test_invalid_code_6(self):
        """
        Test case: An invalid SWIFT code is passed as an argument to the function.
        Example: "AAAABBCC123123"
        Expected behavior: The function should return False because the code exceeds tha valid length.
        """
        result = is_valid_swift_code("AAAABBCC123123")
        self.assertFalse(result)

    def test_invalid_code_7(self):
        """
        Test case: An invalid SWIFT code is passed as an argument to the function.
        Example: "AAAABB"
        Expected behavior: The function should return False because the code is too short.
        """
        result = is_valid_swift_code("AAAABB")
        self.assertFalse(result)

    def test_invalid_code_8(self):
        """
        Test case: An invalid SWIFT code is passed as an argument to the function.
        Example: "aaaabbcc123"
        Expected behavior: The function should return False because the code contains lowercase letters which are not allowed.
        """
        result = is_valid_swift_code("aaaabbcc123")
        self.assertFalse(result)

    def test_valid_code_1(self):
        """
        Test case: A valid SWIFT code is passed as an argument to the function.
        Expected behavior: The function should return True.
        """
        result = is_valid_swift_code("AAAABBCC123")
        self.assertTrue(result)

    def test_valid_code_2(self):
        """
        Test case: A valid SWIFT code is passed as an argument to the function.
        Expected behavior: The function should return True.
        """
        result = is_valid_swift_code("APSBMTMTXXX")
        self.assertTrue(result)

    def test_valid_code_3(self):
        """
        Test case: A valid SWIFT code is passed as an argument to the function.
        Expected behavior: The function should return True.
        """
        result = is_valid_swift_code("BCHICLR10R3")
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
