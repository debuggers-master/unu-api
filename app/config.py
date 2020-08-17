"""
Unu API - Application settings.
"""

from secrets import token_urlsafe
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    General Application settings class.
    """

    class Config:
        """
        Get env variables from dotenv file
        """
        env_file = ".env"

    # APP
    APP_NAME: str = "Unu - API"
    SECRET_KEY: str = token_urlsafe(32)
    API_V1_STR: str = "/api/v1"
    CORS_ORIGIN: str

    # MONGO DB
    DB_NAME: str
    DB_PASSWORD: str
    DB_CLUSER: str
    DB_USERNAME: str

    # SEND_GRIND
    SENDGRID_API_KEY: str

    # STORAGE
    GCP_STORAGE_KEY: str


settings = Settings()
