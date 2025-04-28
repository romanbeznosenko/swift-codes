import os
import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from dotenv import load_dotenv

from main import app
from app.db.database import get_db, Base
from app.models.swift_code import SwiftCodeModel

load_dotenv()

MYSQL_USER: str = os.getenv("MYSQL_USER", "user")
MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "password")
MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
MYSQL_TEST_DATABASE: str = os.getenv("MYSQL_TEST_DATABASE", "test_swift_codes")

TEST_DB_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:3307/{MYSQL_TEST_DATABASE}"


class IntegrationTests(unittest.TestCase):
    """
    Integration test suite for the Swift Codes API.

    This test suite verifies that all API endpoints work correctly, including:
    - Retrieving SWIFT codes by ID (both headquarters and branches)
    - Retrieving SWIFT codes by country
    - Creating new SWIFT codes (with validation)
    - Deleting existing SWIFT codes

    Each test method focuses on a specific aspect of the API's functionality.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up test environment before any tests run.

        Creates a database engine and session factory that will be used for all tests.
        Also creates all database tables needed for testing.
        """

        cls.engine = create_engine(
            TEST_DB_URL,
            poolclass=StaticPool
        )
        cls.TestingSessionLocal = sessionmaker(
            autoflush=False, bind=cls.engine)

        Base.metadata.create_all(bind=cls.engine)

    def setUp(self):
        """
        Set up test environment before each test.

        Creates a new database session, overrides the database dependency,
        initializes the test client, and populates the database with test data.
        """

        self.db = self.TestingSessionLocal()

        def override_get_db():
            try:
                yield self.db
            finally:
                pass

        app.dependency_overrides[get_db] = override_get_db

        self.client = TestClient(app)
        self.setup_test_data()

    def setup_test_data(self):
        """
        Create test data in the database.

        Adds sample SWIFT codes including:
        - A headquarter bank in the US with two branches
        - Another bank in Canada

        This data is used by various test methods to verify API functionality.
        """

        hq = SwiftCodeModel(
            swift_code="AAAAUSCCXXX",
            address="123 Main St, HQ",
            bank_name="Test Bank",
            country_ISO2="US",
            country_name="UNITED STATES",
            is_headquarter=True
        )

        branch1 = SwiftCodeModel(
            swift_code="AAAAUSCC123",
            address="456 Branch Ave",
            bank_name="Test Bank Branch 1",
            country_ISO2="US",
            country_name="UNITED STATES",
            is_headquarter=False
        )

        branch2 = SwiftCodeModel(
            swift_code="AAAAUSCC321",
            address="789 Branch Blvd",
            bank_name="Test Bank Branch 2",
            country_ISO2="US",
            country_name="UNITED STATES",
            is_headquarter=False
        )

        other_bank = SwiftCodeModel(
            swift_code="ZZYYCAWW123",
            address="999 Other St",
            bank_name="Other Bank",
            country_ISO2="CA",
            country_name="CANADA",
            is_headquarter=True
        )

        self.db.add_all([hq, branch1, branch2, other_bank])
        self.db.commit()

    def tearDown(self):
        """
        Clean up after each test.

        Deletes all data from all tables, clears dependency overrides,
        and closes the database session.
        """

        for table in reversed(Base.metadata.sorted_tables):
            self.db.execute(table.delete())
        self.db.commit()

        app.dependency_overrides.clear()

        self.db.close()

    @classmethod
    def tearDownClass(cls):
        """
        Clean up after all tests have run.

        Drops all tables from the test database.
        """

        Base.metadata.drop_all(bind=cls.engine)

    def test_get_swift_code_by_id_headquarter(self):
        """
        Test retrieving a headquarter SWIFT code.

        Verifies that:
        - The response status is 200 OK
        - The correct SWIFT code data is returned
        - The headquarter flag is set to true
        - The response includes a list of branches
        """

        response = self.client.get("/v1/swift-codes/AAAAUSCCXXX")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["swiftCode"], "AAAAUSCCXXX")
        self.assertEqual(data["bankName"], "Test Bank")
        self.assertEqual(data["countryISO2"], "US")
        self.assertTrue(data["isHeadquarter"])
        self.assertIn("branches", data)
        self.assertEqual(len(data["branches"]), 2)

    def test_get_swift_code_by_id_branch(self):
        """
        Test retrieving a branch SWIFT code.

        Verifies that:
        - The response status is 200 OK
        - The correct SWIFT code data is returned
        - The headquarter flag is set to false
        - The response does not include a branches list
        """

        response = self.client.get("/v1/swift-codes/AAAAUSCC123")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["swiftCode"], "AAAAUSCC123")
        self.assertEqual(data["bankName"], "Test Bank Branch 1")
        self.assertEqual(data["countryISO2"], "US")
        self.assertFalse(data["isHeadquarter"])
        self.assertNotIn("branches", data)

    def test_get_swift_code_by_id_not_found(self):
        """
        Test retrieving a non-existent SWIFT code.

        Verifies that:
        - The response status is 404 Not Found
        - The response includes an error detail
        """

        response = self.client.get("/v1/swift-codes/123412431")

        self.assertEqual(response.status_code, 404)
        self.assertIn("detail", response.json())

    def test_get_swift_code_by_country_code(self):
        """
        Test retrieving all SWIFT codes for a specific country.

        Verifies that:
        - The response status is 200 OK
        - The response includes the correct country information
        - The response includes all SWIFT codes for that country
        """

        response = self.client.get("/v1/swift-codes/country/US")

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(data["countryISO2"], "US")
        self.assertEqual(data["countryName"], "UNITED STATES")
        self.assertEqual(len(data["swiftCodes"]), 3)

    def test_get_swift_by_country_not_found(self):
        """
        Test retrieving SWIFT codes for a non-existent country.

        Verifies that:
        - The response status is 404 Not Found
        - The response includes an error detail
        """

        response = self.client.get("/v1/swift-codes/country/ZX")

        self.assertEqual(response.status_code, 404)
        self.assertIn("detail", response.json())

    def test_create_swift_code_success(self):
        """
        Test successfully creating a new SWIFT code.

        Verifies that:
        - The response status is 201 Created
        - The response includes a success message
        - The created SWIFT code can be retrieved using the GET endpoint
        """

        new_code = {
            "address": "Test Address",
            "bankName": "testBank",
            "countryISO2": "FR",
            "countryName": "FRANCE",
            "isHeadquarter": True,
            "swiftCode": "NEWBFRBBXXX"
        }

        response = self.client.post("/v1/swift-codes", json=new_code)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["message"], "SWIFT code record created successfully.")

        get_response = self.client.get("/v1/swift-codes/NEWBFRBBXXX")
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json()["bankName"], "testBank")

    def test_create_swift_code_duplicate(self):
        """
        Test creating a duplicate SWIFT code.

        Verifies that:
        - The response status is 409 Conflict
        - The response includes an error message about duplicate SWIFT code
        """

        duplicate_code = {
            "address": "Duplicate Address",
            "bankName": "Duplicate Bank",
            "countryISO2": "US",
            "countryName": "UNITED STATES",
            "isHeadquarter": False,
            "swiftCode": "AAAAUSCC123"
        }

        response = self.client.post("/v1/swift-codes", json=duplicate_code)

        self.assertEqual(response.status_code, 409)
        self.assertIn("already exists", response.json()["detail"])

    def test_create_swift_code_invalid_fromat(self):
        """
        Test creating a SWIFT code with invalid format.

        Verifies that:
        - The response status is 422 Unprocessable Entity
        - The response includes an error message about invalid format
        """

        invalid_code = {
            "address": "Invalid Address",
            "bankName": "Invalid Bank",
            "countryISO2": "US",
            "countryName": "UNITED STATES",
            "isHeadquarter": False,
            "swiftCode": "INVALID"
        }

        response = self.client.post("/v1/swift-codes", json=invalid_code)

        self.assertEqual(response.status_code, 422)
        self.assertIn("Invalid SWIFT code format",
                      response.json()["detail"][0]["msg"])

    def test_create_swift_code_country_mismatch(self):
        """
        Test creating a SWIFT code with country code mismatch.

        Verifies that:
        - The response status is 422 Unprocessable Entity
        - The response includes an error message about country code mismatch
        """

        mismatch_code = {
            "address": "Mismatch Address",
            "bankName": "Mismatch Bank",
            "countryISO2": "US",
            "countryName": "UNITED STATES",
            "isHeadquarter": False,
            "swiftCode": "TESTFRBB123"
        }

        response = self.client.post("/v1/swift-codes", json=mismatch_code)

        self.assertEqual(response.status_code, 422)
        error_detail = response.json()["detail"]
        self.assertTrue(
            any("Country ISO2 code must match the country code in the SWIFT code" in str(
                error) for error in error_detail),
            f"Expected error message not found in: {error_detail}"
        )

    def test_create_swift_code_invalid_headquarter(self):
        """
        Test creating a SWIFT code with invalid headquarter designation.

        Verifies that:
        - The response status is 422 Unprocessable Entity
        - The response includes an error message about headquarter designation
        """

        invalid_hq = {
            "address": "Invalid HQ",
            "bankName": "Invalid HQ Bank",
            "countryISO2": "DE",
            "countryName": "GERMANY",
            "isHeadquarter": False,
            "swiftCode": "TESTDEBBXXX"
        }

        response = self.client.post("/v1/swift-codes", json=invalid_hq)

        self.assertEqual(response.status_code, 422)
        self.assertIn("'XXX' must be marked as headquarters",
                      response.json()["detail"][0]["msg"])

    def test_delete_swift_code_success(self):
        """
        Test successfully deleting a SWIFT code.

        Verifies that:
        - The response status is 200 OK
        - The response includes a success message
        - The deleted SWIFT code cannot be retrieved using the GET endpoint
        """

        response = self.client.delete("v1/swift-codes/AAAAUSCC123")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["message"], "SWIFT code record deleted successfully")

        get_response = self.client.get("/v1/swift-codes/AAAAUSCC123")
        self.assertEqual(get_response.status_code, 404)

    def test_delete_swift_code_not_found(self):
        """
        Test deleting a non-existent SWIFT code.

        Verifies that:
        - The response status is 404 Not Found
        - The response includes an error message about SWIFT code not found
        """

        response = self.client.delete("v1/swift-codes/NONEXIST")

        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"])


if __name__ == "__main__":
    unittest.main()
