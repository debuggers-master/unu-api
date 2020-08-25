"""
Speakers Schema Models
"""
from typing import Optional, List
from pydantic import BaseModel, Field


class EventId(BaseModel):
    """
    Base Model for request or return eventId
    """
    eventId: str = Field(...,
                         description="UUID of a event")


class SpeakerInfo(BaseModel):
    """
    Base Model to  speakers
    """
    SpeakerName: str = Field(None,
                      description="Name of the speaker",
                      example="Carlos Gonzales")
    SpeakerBio: str = Field(None,
                           description="biography of the speaker",
                           example="Studied at, nowdays is working at")
    twitter: str = Field(None,
                         description="Twitter ",
                         example="DeveloperMax")
    rol: str = Field(None,
                     description="rol of the speaker",
                     example="Backend Developer")


class SpeakerImg(BaseModel):
    """
    Base Model to get str base64 for  speaker photo
    """
    speakerPhoto: str = Field(None,
                              description="encoded base64 image")


class SpeakerDB(SpeakerInfo):
    """
    Base Model to add speaker
    """
    urlSpeakerPhoto : str = Field(None,
                                  description="url of speakerPhoto updloaded to the storage")
    speakerId: str = Field(...,
                           description="UUID of a speaker")


class SpeakerIn(EventId):
    """
    Base Model to add a new speaker
    """
    speakers: Optional[List[SpeakerDB]] = []
