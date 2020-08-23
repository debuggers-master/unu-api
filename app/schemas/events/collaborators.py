"""
Collaboratos Schema Models
"""
from typing import List
from pydantic import BaseModel, Field

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
    collaboratorId: str = Field(None, description="Unique collaborator uuid identifier")


class CollaboratorDelete(EventOut,CollaboratorOut):
    """
    Base Model to delele a collaborator
    """