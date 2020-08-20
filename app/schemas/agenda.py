"""
Events Schema Models
"""

from typing import List, Optional
from pydantic import BaseModel, Field  # pylint: disable-msg=E0611


class ConferenceBase(BaseModel):
    """
    Base Model to add new conferences
    """
    title: str = Field(...,
                       description="name of the conference or speech",
                       example=" The Event App Show")
    description: str = Field(None,
                             description="Text description of event",
                             example="El equipo nos mostrara")
    timetable: str = Field(None,
                           description="Conference schedule",
                           example="1:00pm-3:00pm")
    speakerName: str = Field(None,
                             description="Name of the speaker",
                             example="Carlos Gonzales")

class ConfeenceIn(ConferenceBase):
    """
    Base Model to add new conferences
    """
    eventId: str = Field(...,
                         description="Unique Id of an event",
                         example="string")

class ConferenceDB(ConferenceBase):
    """
    Base Model upload to DB when conference
    is created  and give back when user i
    """
    conferenceID: str = Field(None,
                              description="Unique Id of an event",
                              example="string")


class ConfeenceOut(BaseModel):
    """
    Base Model to add new conferences
    """
    conferenceID: str = Field(...,
                              description="Unique Id of an event",
                              example="string")


class DayIn(BaseModel):
    """
    Base Model Day Events
    """
    day_title: str = Field(...,
                           description=" A Text to show the day of the conference",
                           example="Sunday 30 of agust, 2020")
    date: str = Field(...,
                      description=" A Text to show the day of the conference",
                      example="Sunday 30 of agust, 2020")
    conferences: Optional[List[ConferenceDB]] = []

class DayDB(DayIn):
    """
    Base Model  to save info in DB
    """
    dayId: str = Field(None,
                       description="Unique Id of organization")

class DayOut(BaseModel):
    """
    Base Model  to save info in DB
    """
    dayId: str = Field(None,
                       description="Unique Id of organization")


class Agenda(BaseModel):
    """
    Base Model Day Events
    """
    days: Optional[List[DayDB]] = []
