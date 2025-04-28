from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import SQLAlchemyError
from app.db.database import engine, init_db
from app.models.swift_code import swift_codes
from app.core.parser import parse_swift_data

PATH_TO_CSV = "data/Interns_2025_SWIFT_CODES - Sheet1.csv"


def load_data():
    """
    Load SWIFT code data from CSV into the database.
    """
    init_db()

    try:
        parsed_data = parse_swift_data(PATH_TO_CSV)
        print(f"Successfully parsed {len(parsed_data)} records.")
    except Exception as e:
        print(f"Parse error occured: {e}")
        return False

    try:
        with engine.begin() as conn:
            inserted_count = 0
            for record in parsed_data:
                statement = insert(swift_codes).values(
                    record).prefix_with("IGNORE")
                conn.execute(statement)
                inserted_count += 1
            print(f"Successfully inserted {inserted_count} records.")
        return True
    except SQLAlchemyError as e:
        print(f"Database error occured: {e}")
        return False


if __name__ == "__main__":
    load_data()
