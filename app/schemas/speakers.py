"""
Speakers Events  Schema Models
"""

from pydantic import BaseModel, Field # pylint: disable-msg=E0611

class SpeakerBase(BaseModel):
    """
    Base Model for speaker
    """
    name: str = Field(...,
                      description="full name of speaker",
                      example="Marcos Cooler")

class SpeakerIn(SpeakerBase):
    """
    Base Model to create speaker
    """
    event_id: str = Field(...,
                          description="Unique Id identifier of a event",
                          example="name_last@organization.com")
    rol: str = Field(...,
                     description="rol of speaker",
                     example="Google Devs Expert")
    biography: str = Field(None,
                           description="Biography of speaker",
                           example="Software developer by error .....")
    twitter: str = Field(None,
                         description="Twitter User ",
                         example="programer2020")
    urlPhoto: str = Field(None,
                          description="url of speaker image")


class SpeakerOut(SpeakerBase):
    """
    Base Model to create speaker
    """
