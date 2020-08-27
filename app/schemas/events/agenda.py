"""
Events Schema Models
"""

from typing import Optional, List
from pydantic import BaseModel, Field  # pylint: disable-msg=E0611

from schemas.events.speakers import SpeakerInfo


class EventId(BaseModel):
    """
    Base Model for request or return eventId
    """
    eventId: str = Field(..., description="UUID of a event")


class DayId(BaseModel):
    """
    Base Model for request or return eventId
    """
    dayId: str = Field(..., description="UUID of a day")


class ConferenceInfo(SpeakerInfo):
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


class ConferenceDB(ConferenceInfo):
    """
    Base Model to Conference
    """
    conferenceId: str = Field(
        ...,
        description="UUID of a conference")

    speakerId: str = Field(..., description="The speaker uuid")


class ConferenceIn(EventId, DayId):
    """
    Base Model to add a new conferences
    """
    conferenceData: ConferenceInfo


class ConferenceUpdate(EventId, DayId):
    """
    Base Model to add a new conferences
    """
    conferenceData: ConferenceDB


class ConferenceOnDelete(EventId, DayId):
    """
    Base Model to add a new conferences
    """
    conferenceId: str = Field(...)
    speakerId: str = Field(...)


class DayInfo(BaseModel):
    """
    Principal day info
    """
    date: str = Field(..., description="The start day")


class DaySaved(DayInfo):
    """
    Principal day info
    """
    dayId: str = Field(..., description="The day uuid")


class DayIn(EventId):
    """
    Base Model Day Events
    """
    dayData: DayInfo


class DayUpdate(EventId):
    """
    Body for update a day
    """
    dayData: DaySaved


class DayOnDelete(EventId):
    """
    Body for update a day
    """
    dayId: str = Field(..., description="The day uuid")
