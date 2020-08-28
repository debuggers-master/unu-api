"""
Collaboratos Schema Models
"""

from typing import Optional
from pydantic import BaseModel, Field, EmailStr  # pylint: disable-msg=E0611


class EventId(BaseModel):
    """
    Base Model for request or return eventId.
    """
    eventId: str = Field(...,  description="UUID of a event")


class CollaboratorInfo(BaseModel):
    """
    Base Model of Collaborator information.
    """

    email: EmailStr = Field(
        ...,
        description="Email of user",
        example="stan_lee@marvel.com")

    firstName: str = Field(
        ...,
        description="Name of collaborator",
        example="Stan")

    lastName: str = Field(
        ...,
        description="Lastname of collaborator",
        example="Lee")


class CollaboratorInDb(CollaboratorInfo):
    """
    Base Model to store a Collaborator.
    """
    userId: Optional[str] = Field(description="UUID of the event")
    password: str = Field(..., decription="The collaborator password")


class NewCollaborator(EventId):
    """
    Base Model of body to add a new Collaborator.
    """
    collaboratorData: Optional[CollaboratorInDb]
    email: Optional[str]


class CollaboratorOnDelete(EventId):
    """
    Base Model of body to delete a Collaborator.
    """
    email: str = Field(..., description="The collaborator email")


class CollaboratorInEvent(BaseModel):
    """
    Base Model schema for collaborators in event list.
    """
    email: str
    firstName: str
    lastName: str
