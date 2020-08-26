"""
Events Schema Models
"""

from schemas.events.speakers import SpeakerInfo, SpeakerImg

from typing import Optional, List
from pydantic import BaseModel, Field  # pylint: disable-msg=E0611


class ConferenceInfo(BaseModel):
    """
    Base Model info  conferences
    """
    name: str = Field(None,
                      description="name of the conference or speech",
                      example=" The Event App Show")
    description: str = Field(None,
                             description="Text description of event",
                             example="El equipo nos mostrara")
    startHour: str = Field(None,
                           description="Start Hour",
                           example="13:000")
    endHour: str = Field(None,
                         description="End Hour",
                         example="13:000")


class ConferenceIn(ConferenceInfo, SpeakerInfo, SpeakerImg):
    """
    Base Model to add a new conferences
    """


class ConferenceDB(ConferenceInfo, SpeakerInfo, SpeakerImg):
    """
    Base Model to Conference
    """
    conferenceId: str = Field(...,
                              description="UUID of a conference")


class Day(BaseModel):
    """
    Base Model Day Events
    """
    dayId: str = Field(...,
                       description="UUID of a conference")
    date: str = Field(...,
                      description="Date of day evenet DD/MM/YYYY",
                      example="28/08/2020")
    conference: Optional[List[ConferenceDB]] = []
