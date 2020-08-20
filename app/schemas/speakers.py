"""
Speakers Events  Schema Models
"""

from pydantic import BaseModel, Field  # pylint: disable-msg=E0611


class SpeakerBase(BaseModel):
    """
    Base Model for speaker
    """
    name: str = Field(None,
                      description="full name of speaker",
                      example="Marcos Cooler")
    biography: str = Field(None,
                           description="Biography of speaker",
                           example="Software developer by error .....")
    rol: str = Field(None,
                     description="rol of speaker",
                     example="Google Devs Expert")
    twitter: str = Field(None,
                         description="Twitter User ",
                         example="programer2020")
    urlPhoto: str = Field(None,
                          description="url of speaker image")


class SpeakerIn(SpeakerBase):
    """
    Base Model to create speaker
    """
    eventId: str = Field(...,
                         description="Unique Id of an event",
                         example="string")


class SpeakerOut():
    """
    Base Model return when a speaker is just created
    """
    speakerId: str = Field(...,
                           description="Unique Id of a speaker")
