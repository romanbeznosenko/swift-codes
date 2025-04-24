from sqlalchemy import create_engine, select, MetaData, Table, Column, String, Boolean
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("MYSQL_USER")
PASSWORD = os.getenv("MYSQL_PASSWORD")
HOST = os.getenv("MYSQL_HOST")
PORT = os.getenv("PORT")
DATABASE = os.getenv("MYSQL_DATABASE")

DATABASE_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"


def find_all_branches(swift_code: str) -> List[tuple]:
    statement = select(swift_codes).where(swift_codes.c.swift_code.like(
        f"{swift_code}%") & ~swift_codes.c.swift_code.like("%XXX"))
    
    with engine.begin() as conn:
        result = conn.execute(statement).fetchall()
    
    return result


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

result = find_all_branches("BCHICLRM")
for i in result:
    print(i)
