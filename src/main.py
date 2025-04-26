from sqlalchemy import and_, not_
from sqlalchemy import create_engine, select, MetaData, Table, Column, String, Boolean, delete
import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base

from src.parse import is_valid_swift_code

from pydantic import BaseModel
from typing import List
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os

load_dotenv()

USERNAME = os.getenv("MYSQL_USER")
PASSWORD = os.getenv("MYSQL_PASSWORD")
HOST = os.getenv("MYSQL_HOST")
PORT = os.getenv("PORT")
DATABASE = os.getenv("MYSQL_DATABASE")

DATABASE_URL = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
metadata = MetaData()

Base = declarative_base()

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


class SwiftCode(BaseModel):
    address: str
    bankName: str
    countryISO2: str
    countryName: str
    isHeadquarter: bool
    swiftCode: str


def find_all_branches(swift_code: str) -> List[tuple]:
    swift_base = swift_code[:8]
    print(swift_base)
    statement = select(swift_codes).where(
        and_(
            swift_codes.c.swift_code.like(f"{swift_base}%"),
            not_(swift_codes.c.swift_code.like(f"{swift_base}XXX"))
        )
    )

    with engine.begin() as conn:
        result = conn.execute(statement).fetchall()

    return result


def create_branch_response(data_row: sqlalchemy.engine.row.Row) -> dict:
    branch = {
        "address": data_row.address,
        "bankName": data_row.bank_name,
        "countryISO2": data_row.country_ISO2,
        "isHeadquarter": data_row.is_headquarter,
        "swiftCode": data_row.swift_code
    }
    return branch


app = FastAPI()


@app.get("/v1/swift-codes/{swift_code}")
async def get_swift_code_by_id(swift_code: str):
    with engine.begin() as conn:
        statement = select(swift_codes).where(
            swift_codes.c.swift_code == swift_code)
        result = conn.execute(statement).fetchone()

    if result is None:
        raise HTTPException(status_code=404, detail="No data found.")

    response = {
        "address": result.address,
        "bankName": result.bank_name,
        "countryISO2": result.country_ISO2,
        "countryName": result.country_name,
        "isHeadquarter": result.is_headquarter,
        "swiftCode": result.swift_code
    }

    if response["isHeadquarter"] == True:
        response["branches"] = []
        result = find_all_branches(response["swiftCode"])
        for data_row in result:
            branch = create_branch_response(data_row)
            response["branches"].append(branch)

    return response


@app.get("/v1/swift-codes/country/{countryISO2code}")
async def get_swift_codes_by_country_iso2_code(countryISO2code: str):
    with engine.begin() as conn:
        statement = select(swift_codes).where(
            swift_codes.c.country_ISO2 == countryISO2code)
        result = conn.execute(statement).fetchall()

        statement = select(swift_codes.c.country_name).where(
            swift_codes.c.country_ISO2 == countryISO2code)
        country_name = conn.execute(statement).fetchone()

    if result is None:
        raise HTTPException(status_code=404, detail="No data found.")

    response = {
        "countryISO2": countryISO2code,
        "countryName": country_name[0],
        "swiftCodes": []
    }

    for dataRow in result:
        branch = create_branch_response(dataRow)
        response["swiftCodes"].append(branch)

    return response


@app.post("/v1/swift-codes", status_code=201)
async def create_swift_code_record(swift_code_record: SwiftCode):
    if not is_valid_swift_code(swift_code_record.swiftCode):
        raise HTTPException(
            status_code=400, detail="Invalid SWIFT code format")

    swift_code_record.address = swift_code_record.address.strip()
    swift_code_record.bankName = swift_code_record.bankName.strip()
    swift_code_record.countryISO2 = swift_code_record.countryISO2.strip().upper()
    swift_code_record.countryName = swift_code_record.countryName.strip()

    if len(swift_code_record.countryISO2) != 2:
        raise HTTPException(
            status_code=400, detail="Country ISO2 code must be exactly 2 characters")

    if swift_code_record.countryISO2 != swift_code_record.swiftCode[4:6]:
        raise HTTPException(
            status_code=400, detail="Country ISO2 code must match the country code in the SWIFT code")

    if len(swift_code_record.bankName) < 3:
        raise HTTPException(
            status_code=400, detail="Bank name must be at least 3 characters long")

    if len(swift_code_record.swiftCode) == 11 and swift_code_record.swiftCode[-3:] == "XXX":
        if not swift_code_record.isHeadquarter:
            raise HTTPException(
                status_code=400, detail="SWIFT codes ending with 'XXX' must be marked as headquarters")

    with engine.begin() as conn:
        statement = select(swift_codes).where(
            swift_codes.c.swift_code == swift_code_record.swiftCode)
        existing_record = conn.execute(statement).fetchone()

    if existing_record:
        raise HTTPException(
            status_code=409, detail="SWIFT code already exists in the database")

    try:
        with engine.begin() as conn:
            conn.execute(
                swift_codes.insert().values(
                    swift_code=swift_code_record.swiftCode,
                    address=swift_code_record.address,
                    bank_name=swift_code_record.bankName,
                    country_ISO2=swift_code_record.countryISO2,
                    country_name=swift_code_record.countryName,
                    is_headquarter=swift_code_record.isHeadquarter
                )
            )

        return {"message": "SWIFT code record created successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database error: {str(e)}")


@app.delete("/v1/swift-codes/{swift_code}")
async def delete_swift_code(swift_code: str):
    try:
        with engine.begin() as conn:
            statement = select(swift_codes).where(
                swift_codes.c.swift_code == swift_code)
            existing_record = conn.execute(statement).fetchone()

            if not existing_record:
                raise HTTPException(
                    status_code=404, detail="SWIFT code not found")

            delete_statement = swift_codes.delete().where(
                swift_codes.c.swift_code == swift_code)
            conn.execute(delete_statement)

            return {"message": "SWIFT code record deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Database error: {str(e)}")
