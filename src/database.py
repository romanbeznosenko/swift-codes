from sqlalchemy import create_engine, MetaData, Table, Column, String, Boolean
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import SQLAlchemyError
from src.parse import parse_swift_data
import os
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("MYSQL_USER")
PASSWORD = os.getenv("MYSQL_PASSWORD")
HOST = os.getenv("MYSQL_HOST")
PORT = os.getenv("PORT")
DATABASE = os.getenv("MYSQL_DATABASE")

DATABASE_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
PATH_TO_CSV = "data/Interns_2025_SWIFT_CODES - Sheet1.csv"

if __name__ == "__main__":
    engine = create_engine(DATABASE_URL)
    metadata = MetaData()

    swift_codes = Table("swift_codes", metadata,
                        Column("swift_code", String(11),
                               primary_key=True, unique=True),
                        Column("address", String(255), nullable=True),
                        Column("bank_name", String(255), nullable=True),
                        Column("country_ISO2", String(2), nullable=True),
                        Column("country_name", String(255), nullable=True),
                        Column("is_headquarter", Boolean, default=False),
                        )

    metadata.create_all(engine)

    try:
        parsed_data = parse_swift_data(PATH_TO_CSV)
    except Exception as e:
        print(f"Parse error occured: {e}")

    try:
        with engine.begin() as conn:
            for record in parsed_data:
                statement = insert(swift_codes).values(record).prefix_with("IGNORE")
                conn.execute(statement)
    except SQLAlchemyError as e:
        print(f"Database error occured: {e}")
