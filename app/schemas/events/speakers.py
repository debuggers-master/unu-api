"""
Speakers Schema Models
"""

from typing import Optional
from pydantic import BaseModel, Field  # pylint: disable-msg=E0611


class SpeakerInfo(BaseModel):
    """
    Base Model to  speakers
    """
    speakerName: str = Field(
        ...,
        description="Name of the speaker",
        example="Danil Gonzales")

    speakerBio: str = Field(
        ...,
        description="Biography of the speaker",
        example="Studied at, nowdays is working at")

    twitter: str = Field(
        ...,
        description="Twitter ",
        example="@dani25")

    rol: str = Field(
        ...,
        description="rol of the speaker",
        example="Backend Developer")

    speakerPhoto: str = Field(
        ...,
        description="Speaker image")


class SpeakerDB(SpeakerInfo):
    """
    Speaker in db Model
    """
    speakerId: Optional[str] = Field("", description="The speaker uuid")
