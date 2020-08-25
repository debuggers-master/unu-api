"""
User Schema Models
"""
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field  # pylint: disable-msg=E0611

from .organizations import OrganizationOut


class EventId(BaseModel):
    """
    Base Model for request or return eventId
    """
    eventId: str = Field(...,
                         description="UUID of a event")

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

class EventUserBaseDB(EventUserBase, EventId):
    """
    Base Model to Save  Information
    of event in users document
    """



class UserId(BaseModel):
    """
    Base Model for request or return userId
    """
    userId: str = Field(...,
                         description="UUID of a user")

class CollaboratorDB(UserId):
    """
    User Base to Collaborator Information
    """
    email: EmailStr = Field(...,
                            description="Email of user",
                            example="name_last@organization.com")
    name: str = Field(None,
                      description="Name of collaborator",
                      example="Mario Barbosa")



class UserBase(BaseModel):
    """
    Base Model for user
    """
    email: EmailStr = Field(...,
                            description="Email of user",
                            example="name_last@organization.com")
    firstName: str = Field(None,
                           description="Name of user",
                           example="Mario")
    lastName: str = Field(None,
                          description="Lastname of user",
                          example="Barbosa")


class UserIn(UserBase):
    """
    Base Model for register new user or login , this class extends UserBase
    """
    password: str = Field(...,
                          description="Password of user account")


class UserOut(UserId, UserIn):
    """
    Base Model returned when user is login new,
    """
    Hola : str
    organizations: Optional[List[OrganizationOut]] = []
    myEvents: Optional[List[EventUserBaseDB]] = []
    collaborations: Optional[List[CollaboratorDB]] = []