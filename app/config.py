"""
Unu API - Application settings.
"""

from typing import List
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
    API_V1_STR: str = "/api/v1"
    CORS_ORIGIN: str

    # AUTH
    SECRET_JWT: token_urlsafe(32)

    # MONGO DB
    DB_NAME: str
    DB_PASSWORD: str
    DB_CLUSTER: str
    DB_USERNAME: str

    # SEND_GRIND
    SENDGRID_API_KEY: str

    # STORAGE
    GCP_STORAGE_KEY: str
    GOOGLE_STORAGE_BUCKET: str
    ALLOWED_EXTENSIONS: List[str]
    GOOGLE_APPLICATION_CREDENTIALS: str


settings = Settings()
