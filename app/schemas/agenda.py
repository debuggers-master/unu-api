"""
Events Schema Models
"""

from typing import List
from pydantic import BaseModel, Field # pylint: disable-msg=E0611


class Conference(BaseModel):
    """
    Base Model to add new conferences
    """
    title: str = Field(...,
                       description="name of the conference or speech",
                       example=" The Event App Show")
    description: str = Field(...,
                             description="Text description of event",
                             example="El equipo nos mostrara")
    timetable: str = Field(...,
                           description="Conference schedule",
                           example="1:00pm-3:00pm")
    speakerName: str = Field(...,
                             description="Name of the speaker",
                             example="Carlos Gonzales")

class Day(BaseModel):
    """
    Base Model Day Events
    """
    day_title: str = Field(...,
                           description=" A Text to show the day of the conference",
                           example="Sunday 30 of agust, 2020")
    conference: List[Conference]

class Agenda(BaseModel):
    """
    Base Model Day Events
    """
    days: List[Day]
