from pydantic import BaseModel


class SwiftCodeBase(BaseModel):
    """
    Base SWIFT Code scheme with common attributes
    """

    address: str
    bankName: str
    countryISO2: str
    isHeadquarter: bool
    swiftCode: str
