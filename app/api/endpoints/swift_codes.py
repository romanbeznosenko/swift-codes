from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_, not_
from typing import List, Dict, Any

from app.db.database import get_db
from app.models.swift_code import SwiftCodeModel
from app.schemes.MessageResponse import MessageResponse
from app.schemes.SwiftCodeBase import SwiftCodeBase
from app.schemes.SwiftCodeBranch import SwiftCodeBranch
from app.schemes.SwiftCodeCreate import SwiftCodeCreate
from app.schemes.SwiftCodeResponse import SwiftCodeResponse
from app.schemes.SwiftCodesByCountryResponse import SwiftCodesByCountryResponse
from app.schemes.SwiftCodeWithBranches import SwiftCodeWithBranches


router = APIRouter(prefix="/v1/swift-codes", tags=["swift-codes"])


@router.get("/{swift_code}", response_model=SwiftCodeResponse | SwiftCodeWithBranches)
async def get_swift_code_by_id(swift_code: str, db: Session = Depends(get_db)):
    """
    Retrieve details of a single SWIFT code.
    If the SWIFT code is for a headquarter, it will include branch infromation
    """

    result = db.query(SwiftCodeModel).filter(
        SwiftCodeModel.swift_code == swift_code).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No data found.")

    response_dict = {
        "address": result.address,
        "bankName": result.bank_name,
        "countryISO2": result.country_ISO2,
        "countryName": result.country_name,
        "isHeadquarter": result.is_headquarter,
        "swiftCode": result.swift_code
    }

    if result.is_headquarter:
        response_dict["branches"] = []
        swift_base = result.swift_code[:8]
        branches = db.query(SwiftCodeModel).filter(
            and_(
                SwiftCodeModel.swift_code.like(f"{swift_base}%"),
                SwiftCodeModel.swift_code != result.swift_code,
                not_(SwiftCodeModel.swift_code.like(f"{swift_base}XXX"))
            )
        ).all()

        for branch in branches:
            branch_data = {
                "address": branch.address,
                "bankName": branch.bank_name,
                "countryISO2": branch.country_ISO2,
                "isHeadquarter": branch.is_headquarter,
                "swiftCode": branch.swift_code
            }
            response_dict["branches"].append(branch_data)

        return SwiftCodeWithBranches(**response_dict)
    else:
        return SwiftCodeResponse(**response_dict)


@router.get("/country/{countryISO2code}", response_model=SwiftCodesByCountryResponse)
async def get_swift_codes_by_country_iso2_code(countryISO2code: str, db: Session = Depends(get_db)):
    """
    Return all SWIFT codes with details for a specific country (both headquarters and branches)
    """

    countryISO2code = countryISO2code.strip().upper()

    results = db.query(SwiftCodeModel).filter(
        SwiftCodeModel.country_ISO2 == countryISO2code).all()

    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No data found for the specified country code.")

    country_name = results[0].country_name if results else ""

    swift_codes_list = []
    for result in results:
        swift_code_data = {
            "address": result.address,
            "bankName": result.bank_name,
            "countryISO2": result.country_ISO2,
            "isHeadquarter": result.is_headquarter,
            "swiftCode": result.swift_code
        }
        swift_codes_list.append(swift_code_data)

    response = {
        "countryISO2": countryISO2code,
        "countryName": country_name,
        "swiftCodes": swift_codes_list
    }

    return SwiftCodesByCountryResponse(**response)


@router.post("", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_swift_code_record(swift_code_record: SwiftCodeCreate, db: Session = Depends(get_db)):
    """
    Adds new SWIFT code entries to the database.
    """

    existing_record = db.query(SwiftCodeModel).filter(
        SwiftCodeModel.swift_code == swift_code_record.swiftCode).first()

    if existing_record:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="SWIFT code already exists in the database")

    try:
        new_record = SwiftCodeModel(
            swift_code=swift_code_record.swiftCode,
            address=swift_code_record.address,
            bank_name=swift_code_record.bankName,
            country_ISO2=swift_code_record.countryISO2,
            country_name=swift_code_record.countryName,
            is_headquarter=swift_code_record.isHeadquarter
        )

        db.add(new_record)
        db.commit()

        return MessageResponse(message="SWIFT code record created successfully.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Database error occured: {str(e)}")


@router.delete("/{swift_code}", response_model=MessageResponse)
async def delete_swift_code(swift_code: str, db: Session = Depends(get_db)):
    """
    Deletes a SWIFT code record frmo the database.
    """

    try:
        existsing_record = db.query(SwiftCodeModel).filter(
            SwiftCodeModel.swift_code == swift_code).first()

        if not existsing_record:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="SWIFT code not found.")

        db.delete(existsing_record)
        db.commit()

        return MessageResponse(message="SWIFT code record deleted successfully")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Database error occured: {str(e)}")
