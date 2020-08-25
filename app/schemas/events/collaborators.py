"""
Collaboratos Schema Models
"""
from pydantic import BaseModel, Field, EmailStr

from schemas.users import UserBase


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
    email: EmailStr = Field(...,
                            description="Email of user",
                            example="name_last@organization.com")
    name: str = Field(None,
                      description="Name of collaborator",
                      example="Mario Barbosa")


class CollaboratorDB(CollaboratorInfo):
    """
    Base Model to add Collaborators
    """
    collaboratorId: str = Field(None,
                                description="Unique collaborator uuid identifier")


class CollaboratorOut(BaseModel):
    """
    Base Model returned when a new collaborator is just added
    """
    collaboratorId: str = Field(None,
                                description="Unique collaborator uuid identifier")


class CollaboratorDelete(EventId,CollaboratorOut):
    """
    Base Model to delele a collaborator
    """


class CollaboratorData(BaseModel):
    """
    Base Model Collaboration Data
    """
    email: EmailStr = Field(None,
                            description="Email of user",
                            example="name_last@organization.com")
    firstName: str = Field(None,
                           description="Name of user",
                           example="Mario")
    lastName: str = Field(None,
                          description="Lastname of user",
                          example="Barbosa")


class CollaboratorUpdate(CollaboratorDelete):
    """
    Base Model to update a collaborator
    """
    collaboratorData: CollaboratorData
