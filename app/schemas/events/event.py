"""
Events Schema Models
"""
from typing import Optional, List, Type
from enum import Enum
from pydantic import BaseModel, Field  # pylint: disable-msg=E0611

# from schemas.events.speakers import SpeakerDB
# from schemas.events.agenda import Day
# from schemas.events.associates import AsociateDB
# from schemas.events.collaborators import CollaboratorDB


class EventId(BaseModel):
    """
    Base Model for request or return eventId
    """
    eventId: str = Field(...,
                         description="UUID of a event")


class EventInUser(EventId):
    """
    Schema for event in user.
    """
    name: str
    shortDescription: str
    organizationName: str


class NewEvent(BaseModel):
    """
    Base model for create a new events
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
        example="Eveneto para programar en python")


class EventBasicInfo(BaseModel):
    """
    Base info for events
    """
    name: Optional[str]
    shortDescription: Optional[str]
    description: Optional[str]
    titleHeader: Optional[str]
    imageHeader: Optional[str]
    imageEvent: Optional[str]
    localTime: Optional[str]


class EventOut(EventBasicInfo):
    """
    Base Model for event
    """
    eventId: Optional[str]
    organizationName: Optional[str]
    organizationUrl: Optional[str]
    template: Optional[str]
    url: Optional[str]
    startDate: Optional[str]
    organizationName: Optional[str]

    speakers: Optional[List[dict]]
    agenda: Optional[List[dict]]
    associates: Optional[List[dict]]
    collaborators: Optional[List[dict]]

    publicationStatus: Optional[bool]


class EventIn(BaseModel):
    """
    Base model For recive event Body
    """
    eventId: str = Field(..., description="The event id")
    eventData: EventBasicInfo = Field(...)
