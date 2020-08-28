"""
Unu API - Application settings.
"""

from typing import List
from secrets import token_urlsafe

from pydantic import BaseSettings


###########################################
##       General Configurations          ##
###########################################

class Settings(BaseSettings):
    """
    General Application settings class.
    """

    class Config:
        """
        Get env variables from dotenv file.
        """
        env_file = ".env"

    # ---- APP ---- #
    APP_NAME: str = "Unu - API"
    API_V1_STR: str = "/api/v1"
    CORS_ORIGIN: List[str]
    HOST: str = " http://35.239.16.11"

    # --- AUTH --- #
    SECRET_JWT: str = token_urlsafe(32)

    # ---- DB --- #
    DB_NAME: str
    DB_PASSWORD: str
    DB_CLUSTER: str
    DB_USERNAME: str

    # --- SEND_GRIND --- #
    SENDGRID_API_KEY: str
    EMAIL_SENDER: str = "unu.events@gmail.com"

    # --- REDIS_WORKER --- #
    REDIS_URL: str
    QUEUES: List[str]

    # --- STORAGE --- #
    GOOGLE_STORAGE_BUCKET: str
    ALLOWED_EXTENSIONS: List[str]
    GOOGLE_APPLICATION_CREDENTIALS: str


settings = Settings()
