import time
import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from app.models.swift_code import swift_codes
from app.core.parser import parse_swift_data


DB_USER = os.getenv("MYSQL_USER")
DB_PASSWORD = os.getenv("MYSQL_PASSWORD")
DB_HOST = os.getenv("MYSQL_HOST")
DB_PORT = os.getenv("MYSQL_PORT", "3306")
DB_NAME = os.getenv("MYSQL_DATABASE")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
PATH_TO_CSV = "data/Interns_2025_SWIFT_CODES - Sheet1.csv"


def wait_for_db(max_retries=20, delay=3):
    """
    Wait for database to be available
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
    Load SWIFT codes from CSV
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
