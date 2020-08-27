"""
Collaboratos Schema Models
"""

from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class EventId(BaseModel):
    """
    Base Model for request or return eventId
    """
    eventId: str = Field(...,
                         description="UUID of a event")


class CollaboratorInfo(BaseModel):
    """
    User Base to Collaborator Information
    """

    email: EmailStr = Field(
        ...,
        description="Email of user",
        example="name_last@organization.com")

    firstName: str = Field(
        ...,
        description="Name of collaborator",
        example="Bruce")

    lastName: str = Field(
        ...,
        description="Lastname of collaborator",
        example="Banner")


class CollaboratorInDb(CollaboratorInfo):
    """
    Schema or collaborator in db
    """
    userId: Optional[str]
    password: str = Field(..., decription="The collaborator password")


class NewCollaborator(EventId):
    """
    Body for new collaborator
    """
    collaboratorData: Optional[CollaboratorInDb]
    email: Optional[str]


class CollaboratorOnDelete(EventId):
    """
    Body for delete a collaborator
    """
    email: str = Field(..., description="The collaborator email")
