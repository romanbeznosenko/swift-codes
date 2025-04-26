from app.schemes.SwiftCodeBase import SwiftCodeBase


class SwiftCodeResponse(SwiftCodeBase):
    """
    Scheme for a single Swift Code response (non-headquarter)
    """

    countryName: str

    class Config:
        from_attributes = True
