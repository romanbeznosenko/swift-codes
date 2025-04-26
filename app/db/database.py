from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

settings = get_settings()

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()
metadata = MetaData()


def get_db():
    """
    Dependency function to get a database session.
    Used with FastAPI Depends to manage session lifecycle.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database if they don't exist.
    Used during application startup.
    """

    from app.models.swift_code import SwiftCodeModel
    Base.metadata.create_all(bind=engine)

def test_connection():
    """
    Try database connection, return True if successful.
    """

    try:
        with engine.begin() as conn:
            conn.execute("SELECT 1")
        return True 
    except Exception as e:
        print(f"Database connection error: {e}")
        return False