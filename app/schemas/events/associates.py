"""
Associates schema Models
"""
from typing import Optional
from pydantic import BaseModel, Field


class EventId(BaseModel):
    """
    Base Model for request or return eventId
    """
    eventId: str = Field(...,
                         description="UUID of a event")


class AssociatedInfo(BaseModel):
    """
    Base Model to add Associate
    """
    name: str = Field(None,
                      description="Name of Associate",
                      example="Platzi")
    url: str = Field(None,
                     description="Web page of associate",
                     example="platzi.com")
    logo: str = Field(None,
                      description="encoded base64 image")


class AssociatedInDb(AssociatedInfo):
    """
    Base Model to add Associate
    """
    associatedId: str = Field(..., description="The associated uuid")


class AssociatedIn(EventId):
    """
    Body for add associated to an event
    """
    associatedData: AssociatedInfo


class AssociatedUpdate(EventId):
    """
    Base Model to add a update a associated
    """
    associatedData: AssociatedInDb


class AssociatedOnDelete(EventId):
    """
    Base Model to update a associated
    """
    associatedId: str = Field(..., description="The associated uuid")
