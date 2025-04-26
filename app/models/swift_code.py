from sqlalchemy import Column, String, Boolean, Index
from sqlalchemy.sql import expression
from app.db.database import Base, metadata


class SwiftCodeModel(Base):
    """
    SQLAlchemy model for swift_codes table.

    Represents a SWIFT/BIC11 code entry for a bank branch or headquarters.
    """

    __tablename__ = "swift_codes"

    swift_code = Column(String(11), primary_key=True,
                        unique=True, nullable=False, index=True)
    address = Column(String(255), nullable=True)
    bank_name = Column(String(255), nullable=True)
    country_ISO2 = Column(String(2), nullable=True, index=True)
    country_name = Column(String(255), nullable=True)
    is_headquarter = Column(
        Boolean, server_default=expression.false(), nullable=False)

    def __repr__(self):
        """
        String representation of a SWIFT code
        """

        return f"<SwiftCode {self.swift_code} ({self.bank_name})"


swift_codes = metadata.tables.get("swift_codes")

if swift_codes is None:
    from sqlalchemy import Table, Column, String, Boolean, MetaData
    from app.db.database import metadata

    swift_codes = Table(
        "swift_codes", metadata,
        Column("swift_code", String(11), primary_key=True, unique=True),
        Column("address", String(255), nullable=True),
        Column("bank_name", String(255), nullable=True),
        Column("country_ISO2", String(2), nullable=True),
        Column("country_name", String(255), nullable=True),
        Column("is_headquarter", Boolean, server_default=expression.false(),
               nullable=False)
    )

    Index("idx_swift_code", swift_codes.c.swift_code)
    Index("idx_country_iso2", swift_codes.c.country_ISO2)
