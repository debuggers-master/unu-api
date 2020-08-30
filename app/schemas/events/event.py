"""
Events Schema Models
"""
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field  # pylint: disable-msg=E0611

from schemas.events.speakers import SpeakerDB
from schemas.events.agenda import Day
from schemas.events.associates import AssociatedInDb
from schemas.events.collaborators import CollaboratorInEvent


class EventId(BaseModel):
    """
    Base Model for request or return eventId
    """
    eventId: str = Field(...,
                         description="UUID of a event")


class EventInUser(EventId):
    """
    Base Model schema for event in user.
    """
    name: str
    shortDescription: str
    organizationName: str


class NewEvent(BaseModel):
    """
    Base model of body for create a new event.
    """
    name: str = Field(..., description="The event name")
    template: str = Field(..., description="The choosen template")
    url: str = Field(..., description="The event url")
    startDate: str = Field(..., description="The event start date")
    organizationName: str = Field(..., description="The organization name")


class Templates(str, Enum):
    """
    Template choice list
    """
    template1 = "template1"
    template2 = "template2"


class EventUserBase(BaseModel):
    """
    Base Model to form Information
    of event in users document
    """
    name: str = Field(
        ...,
        description="Name of event",
        example="Python Week Code")

    organizationName: str = Field(
        ...,
        description="Name of organization",
        example="Cosas de ingenieros")

    shortDescription: str = Field(
        ...,
        description="a short description of the event",
        example="Aprende a programar un uno de los mejores lenguajes")


class EventBasicInfo(BaseModel):
    """
    Base info for events
    """
    name: Optional[str] = Field(description="The event name")
    shortDescription: Optional[str] = Field(description="A short description")
    description: Optional[str] = Field(description="Event description")
    titleHeader: Optional[str] = Field(description="Event title")
    imageHeader: Optional[str] = Field(description="Banner image")
    imageEvent: Optional[str] = Field(description="A related image")
    localTime: Optional[str] = Field(
        description="The UTC time of the event eg.(-5)")


class EventOut(EventBasicInfo):
    """
    Base Model for event response.
    """
    eventId: Optional[str]
    organizationName: Optional[str]
    organizationUrl: Optional[str]
    template: Optional[str]
    url: Optional[str]
    startDate: Optional[str]
    organizationName: Optional[str]

    speakers: Optional[List[SpeakerDB]]
    agenda: Optional[List[Day]]
    associates: Optional[List[AssociatedInDb]]
    collaborators: Optional[List[CollaboratorInEvent]]

    publicationStatus: Optional[bool]


class EventIn(BaseModel):
    """
    Base model of body for event calls.
    """
    eventId: str = Field(..., description="The event id")
    eventData: EventBasicInfo = Field(...)


class EventPublishOut(BaseModel):
    """
    Base model of return events publish info
    """
    eventId: str = Field(..., description=" uuid of the event")
    name: Optional[str] = Field(description="The event name")
    startDate: str = Field(..., description="The event start date")
    organizationName: str = Field(..., description="The organization name")
    publicationStatus: Optional[bool]
    shortDescription: Optional[str]
    imageEvent: Optional[str]
