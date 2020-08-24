"""
Speakers Schema Models
"""

from pydantic import BaseModel, Field

from schemas.events.events  import EventOut


class SpeakerInfo(BaseModel):
    """
    Base Model to add speakers
    """
    name: str = Field(None,
                      description="Name of the speaker",
                      example="Marcos")
    biography: str = Field(None,
                           description="biography of the speaker",
                           example="Studied at, nowdays is working at")
    rol: str = Field(None,
                     description="rol of the speaker",
                     example="Backend Developer")
    twitter: str = Field(None,
                         description="Twitter ",
                         example="DeveloperMax")
    photo: str = Field(None,
                         description="base64 encoded photo ")

class SpeakerIn(EventOut):
    """

    """

class SpeakerOut(BaseModel):
    """

    """

class SpeakerDelete(BaseModel):
    """

    """

class SpeakerUpdate(BaseModel):
    """
    
    """