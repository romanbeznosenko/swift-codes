# SWIFT Codes API

This project implements a RESTful API for managing SWIFT/BIC11 (Bank Identifier Code) data. It provides endpoints for retrieving, creating, and deleting SWIFT codes, with validation according to international standards.

## Project Overview

This API allows users to:
- Retrieve details of a specific SWIFT code
- Retrieve all SWIFT codes for a specific country
- Add new SWIFT code entries
- Delete existing SWIFT code entries

The application parses SWIFT code data from a CSV file, stores it in a MySQL database, and exposes it through RESTful endpoints.

## Project Structure
```
swift-codes-api/  
├── app/  
│   ├── api/  
│   │   └── endpoints/  
│   │       └── swift_codes.py    # API endpoint definitions  
│   ├── core/  
│   │   ├── parser.py            # CSV parsing logic 
|   |   └── config.py            # Database configuration file
│   ├── db/  
│   │   ├── database.py          # Database connection management  
|   |   └── load_data.py         # Loading SWIFT entries from CSV to Database logic
│   ├── models/  
│   │   └── swift_code.py        # SQLAlchemy database models  
│   ├── schemes/                 # Pydantic validation schemas  
│   │   ├── MessageResponse.py  
│   │   ├── SwiftCodeBase.py  
│   │   ├── SwiftCodeBranch.py  
│   │   ├── SwiftCodeCreate.py  
│   │   ├── SwiftCodeResponse.py  
│   │   ├── SwiftCodesByCountryResponse.py
│   │   └── SwiftCodeWithBranches.py
│   └── utils/
│       └── validators.py        # SWIFT code validation functions
├── custom_exceptions/           # Custom exception classes
├── data/                        # CSV data files
│   └── Interns_2025_SWIFT_CODES - Sheet1.csv
├── scripts/
│   └── load_data.py             # Script to load data from CSV to database
├── test/                        # Test files
│   ├── test_api_integration_test.py
│   ├── test_is_valid_swift_code.py
│   └── test_parse_swift_data.py
├── .env                         # Environment variables
├── main.py                      # Application entry point
├── Dockerfile                   # Container definition
├── docker-compose.yml           # Container orchestration
└── requirements.txt             # Python dependencies
```

## Prerequisites

- Docker and Docker Compose
- Python 3.11+
- MySQL 8.0+

## Running the Application

### Using Docker (Recommended)
1. Clone the repository
    ```
    git clone https://github.com/romanbeznosenko/swift-codes
    cd swift-codes
    ```
2. Build and start the containers
    ```
    docker-compose up -d
    ```
3. The API will be available at the http://localhost:8080

## Data parsing
The application includes a parser that processes SWIFT code data from CSV files. The parser:
1. **Reads and validates CSV format**
    - Checks for required columns: 'SWIFT CODE', 'COUNTRY ISO2 CODE', 'COUNTRY NAME', 'NAME', 'ADDRESS'
    - Validates that all SWIFT codes follow the correct format
    - Ensures there are no duplicate SWIFT codes
2. **Applies buisiness rules**
    - Identifies headquarters by SWIFT codes ending with 'XXX'
    - Standartizes data formatting (uppercase country codes and names)
    - Associates branch codes with headquarters codes
3. **Handles errors gracefully**
    - Missing columns
    - Invalid SWIFT code formats
    - Duplicate entries
    - File access issues
The parser can be used independently of the API for data preparation and validation.

## CSV Format Requirements
The CSV file should have the following columns:
- `SWIFT CODE`: The SWIFT/BIC11 code (required)
- `COUNTRY ISO2 CODE`: Two-letter ISO country code (required)
- `COUNTRY NAME`: Full name of the country (required)
- `NAME`: Name of the bank or branch (required)
- `ADDRESS`: Physical address (required)

## Running the Parser Independently
To parse a CSV file without loading it into the database:  
```
python -c "from app.core.parser import parse_swift_data; result = parse_swift_data('path/to/your/file.csv'); print(result)"
```

# API Endpoints
## 1. Get SWIFT Code Details
### Endpoint: `GET /v1/swift-codes/{swift-code}`
Retrieves details for a specific SWIFT code. If the code is for a headquarters, it will also include a list of branch codes.

**Example Response for Headquarter**
```json
{
  "address": "123 MAIN ST, HQ",
  "bankName": "TEST BANK",
  "countryISO2": "US",
  "countryName": "UNITED STATES",
  "isHeadquarter": true,
  "swiftCode": "AAAAUSCCXXX",
  "branches": [
    {
      "address": "456 BRANCH AVE",
      "bankName": "TEST BANK BRANCH 1",
      "countryISO2": "US",
      "isHeadquarter": false,
      "swiftCode": "AAAAUSCC123"
    },
    {
      "address": "789 BRANCH BLVD",
      "bankName": "TEST BANK BRANCH 2",
      "countryISO2": "US",
      "isHeadquarter": false,
      "swiftCode": "AAAAUSCC321"
    }
  ]
}
```

## 2. Get SWIFT Code by Country
### Endpoint `GET /v1/swift-codes/country/{countryISO2code}`
Retrieves all SWIFT codes for a specific country  
**Example Response**
```json
{
  "countryISO2": "US",
  "countryName": "UNITED STATES",
  "swiftCodes": [
    {
      "address": "123 MAIN ST, HQ",
      "bankName": "TEST BANK",
      "countryISO2": "US",
      "isHeadquarter": true,
      "swiftCode": "AAAAUSCCXXX"
    },
    {
      "address": "456 BRANCH AVE",
      "bankName": "TEST BANK BRANCH 1",
      "countryISO2": "US",
      "isHeadquarter": false,
      "swiftCode": "AAAAUSCC123"
    }
  ]
}
```

## 3. Create SWIFT Code
### Endpoint `POST /v1/swift-codes`
Creates a new SWIFT code entry:  

**Request body**
```json
{
  "address": "New Address",
  "bankName": "New Bank",
  "countryISO2": "FR",
  "countryName": "FRANCE",
  "isHeadquarter": true,
  "swiftCode": "NEWBFRBBXXX"
}
```

**Response**
```json
{
  "message": "SWIFT code record created successfully."
}
```

## 4. Delete SWIFT Code
### Endpoint `DELETE /v1/swift-codes/{swift-code}`

Delete a SWIFT code entry.

**Response**
```json
{
  "message": "SWIFT code record deleted successfully"
}
```

## Running Tests

### Integration Test with Docker Test Database

The integration test requires a test database. A separate test database container is included in the docker-compose.yml file.

1. Start the test database container:
``` bash
docker-compose up -d mysql_test
```
2. Install dependencies
``` bash
pip install -r requirements.txt
```
3. Run the integration tests:
``` bash
python -m unittest test.test_api_integration_test
```

### Unit Tests
Unit tests can be run independently of the database

Install dependencies
``` bash
pip install -r requirements.txt
```

``` bash
# Run SWIFT code validation tests
python -m unittest test.IsValidSwiftCodeTest

# Run parsing tests
python -m unittest test.ParseSwiftDataTest
```

