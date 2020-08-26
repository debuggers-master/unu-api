"""
Events Schema Models
"""
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, Field  # pylint: disable-msg=E0611

from schemas.events.speakers import SpeakerDB
from schemas.events.agenda import Day
from schemas.events.associates import AsociateDB
from schemas.events.collaborators import CollaboratorDB


class EventId(BaseModel):
    """
    Base Model for request or return eventId
    """
    eventId: str = Field(...,
                         description="UUID of a event")


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
    name: str = Field(...,
                      description="Name of event",
                      example="Python Week Code")
    organizationName: str = Field(...,
                                  description="Name of organization",
                                  example="Cosas de ingenieros")
    shortDescription: str = Field(None,
                                  description="a short description of the event",
                                  example="Eveneto para programar en python")


class EventBase(EventUserBase):
    """
    Base Model for event
    """
    organizationId: str = Field(...,
                                description="UUID of organization")
    description: str = Field(None,
                             description="description of the event",
                             example="Este evento ........")
    imageHeader: str = Field(None,
                             description="encoded base64 image")
    imageEvent: str = Field(None,
                            description="encoded base64 image")
    localTime: str = Field(None,
                           description="UTC of event localization",
                           example="UTC -5")
    speakers: Optional[List[SpeakerDB]] = []
    agenda: Optional[List[Day]] = []
    associates: Optional[List[AsociateDB]] = []
    collaborators: Optional[List[CollaboratorDB]] = []
    publicationStatus: bool = Field(False,
                                    description="True if is accesible to all public",
                                    example=False)
