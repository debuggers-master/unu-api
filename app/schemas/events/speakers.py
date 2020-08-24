"""
Speakers Schema Models
"""

from typing import Optional
from pydantic import BaseModel, Field

from schemas.events.events  import EventOut


class SpeakerInfo(BaseModel):
    """
    Base Model to  speakers
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

class SpeakerIn(EventOut):
    """
    Base Model to add speaker
    """
    spekerInfo: SpeakerInfo
    photo: str = Field(None,
                       description="base64 encoded photo ")

class SpeakerOut(BaseModel):
    """
    Base Model returned when a new associate is just added
    """
    speakerId: str = Field(...,
                             description="Unique speaker uuid identifier")
    url_photo: str = Field(None,
                          description="Unique speaker uuid identifier")

class SpeakerDelete(EventOut, SpeakerOut):
    """
    Base Model to delele a speaker
    """

class SpeakerUpdate(SpeakerDelete):
    """
    Base Model to update a speaker
    """
    speakerInfo: Optional[SpeakerInfo]
