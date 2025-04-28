"""
SWIFT Codes Data Loader

This script loads SWIFT code data from a CSV file into a database. It handles database
connection management, data parsing, and bulk insertion of records.

The script will wait for the database to be available before attempting to load data,
making it suitable for use in containerized environments where the database may start
after this script.
"""


import time
import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from app.core.parser import parse_swift_data
from app.models.swift_code import swift_codes


DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_HOST = os.getenv("MYSQL_HOST")
DB_PORT = os.getenv("MYSQL_PORT", "3306")
DB_NAME = os.getenv("MYSQL_DATABASE")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
PATH_TO_CSV = "data/Interns_2025_SWIFT_CODES - Sheet1.csv"


def wait_for_db(max_retries=20, delay=3):
    """
    Wait for database to be available before proceeding.

    This function attempts to connect to the database repeatedly until successful
    or until the maximum number of retries is reached. This is particularly useful
    in containerized environments where the database may not be immediately available.

    Args:
        max_retries (int): Maximum number of connection attempts (default: 20)
        delay (int): Delay in seconds between attempts (default: 3)

    Returns:
        SQLAlchemy Engine: A configured SQLAlchemy engine connected to the database

    Raises:
        Exception: If unable to connect to the database after all retries
    """

    print("Waiting for database to be ready...")
    engine = create_engine(DATABASE_URL)

    for i in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                print("Database is ready.")
                return engine
        except OperationalError as e:
            print(
                f"Database not available yet, retrying... {i + 1}/{max_retries}")
            time.sleep(delay)

    raise Exception("Failed to connect to database after multiple attempts.")


def load_data(engine):
    """
    Load SWIFT codes from CSV file into the database.
    
    This function parses the CSV file containing SWIFT code data,
    then inserts the data into the database. It uses the IGNORE prefix
    to avoid errors when inserting duplicate records.
    
    Args:
        engine (SQLAlchemy Engine): Database engine to use for insertion
        
    Returns:
        bool: True if data was loaded successfully, False otherwise
    """
    
    try:
        parsed_data = parse_swift_data(PATH_TO_CSV)
        print(f"Successfully parsed {len(parsed_data)} records")
    except Exception as e:
        print(f"Parse error occurred: {str(e)}")
        return False

    try:
        from sqlalchemy.dialects.mysql import insert

        with engine.begin() as conn:
            inserted_records = 0
            for record in parsed_data:
                statement = insert(swift_codes).values(
                    record).prefix_with("IGNORE")
                conn.execute(statement)
                inserted_records += 1
            print(f"Successfully inserted {inserted_records} records")
        return True
    except Exception as e:
        print(f"Database error occurred: {str(e)}")
        return False


if __name__ == "__main__":
    try:
        engine = wait_for_db()

        from app.db.database import Base, metadata

        metadata.create_all(engine)
        success = load_data(engine)

        if success:
            print("Data loaded successfully")
        else:
            print("Failed to load data")
    except Exception as e:
        print(f"Error during data loading process: {str(e)}")
