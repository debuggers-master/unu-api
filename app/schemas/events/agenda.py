"""
Events Schema Models
"""

from typing import List
from pydantic import BaseModel, Field  # pylint: disable-msg=E0611

from schemas.events.speakers import SpeakerInfo


class EventId(BaseModel):
    """
    Base Model for request or return event.
    """
    eventId: str = Field(..., description="UUID of a event")


class DayId(BaseModel):
    """
    Base Model for request a day.
    """
    dayId: str = Field(..., description="UUID of a day")


class ConferenceInfo(SpeakerInfo):
    """
    Base Model info conferences for request body.
    """
    name: str = Field(
        None,
        description="name of the conference or speech",
        example=" The Event App Show")

    description: str = Field(
        None,
        description="Text description of event",
        example="El equipo nos mostrara")

    startHour: str = Field(
        None,
        description="Js String start hour",
        example="Sat Sep 26 2020 9:00:00 GMT-0500 (Central Daylight Time)")

    endHour: str = Field(
        None,
        description="Js String end hour",
        example="Sat Sep 26 2020 10:00:00 GMT-0500 (Central Daylight Time)")


class ConferenceDB(ConferenceInfo):
    """
    Base Model to store Conference
    """
    conferenceId: str = Field(..., description="UUID of a conference")
    speakerId: str = Field(..., description="The speaker uuid")


class ConferenceIn(EventId, DayId):
    """
    Base Model of request body to add a new conferences.
    """
    conferenceData: ConferenceInfo


class ConferenceUpdate(EventId, DayId):
    """
    Base Model of request body to update a conferences.
    """
    conferenceData: ConferenceDB


class ConferenceOnDelete(EventId, DayId):
    """
    Base Model of request body to delete a conference.
    """
    conferenceId: str = Field(...)
    speakerId: str = Field(...)


class DayInfo(BaseModel):
    """
    Principal day info.
    """
    date: str = Field(..., description="The start day")


class DaySaved(DayInfo):
    """
    Principal day info in db.
    """
    dayId: str = Field(..., description="The day uuid")


class DayIn(EventId):
    """
    Base Model of request body to add a day.
    """
    dayData: DayInfo


class DayUpdate(EventId):
    """
    Base Model of request body to update a day.
    """
    dayData: DaySaved


class DayOnDelete(EventId):
    """
    Base Model of request body to delte a day.
    """
    dayId: str = Field(..., description="The day uuid")


class Day(DayId, DayInfo):
    """
    Day in DB model.
    """
    conferences: List[dict]
