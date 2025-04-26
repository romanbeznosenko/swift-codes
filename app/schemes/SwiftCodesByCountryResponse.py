from pydantic import BaseModel, Field
from typing import List
from app.schemes.SwiftCodeBranch import SwiftCodeBranch


class SwiftCodesByCountryResponse(BaseModel):
    """
    Scheme for response when getting Swift Codes by country
    """

    countryISO2: str
    countryName: str
    swiftCodes: List[SwiftCodeBranch] = Field(..., alias="swiftCodes")

    class Config:
        from_attributes = True
