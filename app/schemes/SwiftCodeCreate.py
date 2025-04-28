from pydantic import BaseModel, field_validator, ValidationInfo, model_validator
from app.utils.validators import is_valid_swift_code


class SwiftCodeCreate(BaseModel):
    """
    Scheme for creating a new SWIFT Code
    """

    address: str
    bankName: str
    countryISO2: str
    countryName: str
    isHeadquarter: bool
    swiftCode: str

    @field_validator('swiftCode')
    def validate_swift_code(cls, v):
        if not is_valid_swift_code(v):
            raise ValueError('Invalid SWIFT code format')
        return v
    
    @model_validator(mode='after')
    def validate_fields_together(self):
        if self.swiftCode and self.countryISO2:
            if self.countryISO2 != self.swiftCode[4:6]:
                raise ValueError("Country ISO2 code must match the country code in the SWIFT code")
        
        if self.swiftCode and len(self.swiftCode) == 11 and self.swiftCode[-3:] == "XXX" and not self.isHeadquarter:
            raise ValueError("SWIFT codes ending with 'XXX' must be marked as headquarters")
            
        return self

    @field_validator('countryISO2')
    def validate_country_code(cls, v, info: ValidationInfo):
        v = v.strip().upper()
        if (len(v) != 2):
            raise ValueError("Country ISO2 code must be exactly 2 characters")

        swift_code = info.data.get('swiftCode') if hasattr(info, 'data') else None
        if swift_code:
            if v != swift_code[4:6]:
                raise ValueError(
                    "Country ISO2 code must match the country code in the SWIFT code")
        return v

    @field_validator('isHeadquarter')
    def validate_headquarter(cls, v, info: ValidationInfo):
        swift_code = info.data.get('swiftCode') if hasattr(info, 'data') else None
        if swift_code:
            if len(swift_code) == 11 and swift_code[-3:] == "XXX" and not v:
                raise ValueError(
                    "SWIFT codes ending with 'XXX' must be marked as headquarters")
        return v

    @field_validator('address', 'countryName')
    def strip_strings(cls, v):
        return v.strip() if v else v