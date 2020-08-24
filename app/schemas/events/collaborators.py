"""
Collaboratos Schema Models
"""
from pydantic import BaseModel, Field, EmailStr

from schemas.users import UserBase
from schemas.events.events  import EventOut


class CollaboratorIn(EventOut):
    """
    Base Model to add Collaborators
    """
    collaboratorInfo: UserBase


class CollaboratorOut(BaseModel):
    """
    Base Model returned when a new collaborator is just added
    """
    collaboratorId: str = Field(None,
                                description="Unique collaborator uuid identifier")


class CollaboratorDelete(EventOut,CollaboratorOut):
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

