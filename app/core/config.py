import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables
    """

    MYSQL_USER: str = os.getenv("MYSQL_USER", "user")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "password")
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT: str = os.getenv("PORT", "3306")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "swift_codes")

    MYSQL_ROOT_PASSWORD: str = os.getenv("MYSQL_ROOT_PASSWORD", "rootpassword")
    MYSQL_TEST_DATABASE: str = os.getenv("MYSQL_TEST_DATABASE", "test_swift_codes")
    PORT: str = os.getenv("PORT", "3306")

    @property
    def DATABASE_URL(self):
        """
        Construct database URL from components
        """

        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    """
    Get cached settings singleton
    """

    return Settings()
