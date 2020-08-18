"""
User Schema Models
"""
from typing import List
from pydantic import BaseModel, EmailStr, Field # pylint: disable-msg=E0611

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
    Base Model for register new, this class extends UserBase
    """
    password: str = Field(...,
                          description="Password of user account")

class Organization():
    """
    Base Model for organization dictionary  when user are just login
    """
    organization_id: str = Field(...,
                                 description="Unique Id identifier for organization")
    name: str = Field(...,
                      description="Password of user account",
                      example="Cosas de ingenieros")

class Collaboration():
    """
    Base Model for collaboration dictionary  when user are just login
    """
    event_id: str = Field(...,
                          description="Unique Id identifier for organization")
    url: str = Field(...,
                     description="event url identifier",
                     example="cosas-de-inges/py-week")
    name: str = Field(...,
                      description="event name identifier",
                      example="Python code Week")

class UserOut(UserBase):
    """
    Base Model returned when user is login new, this class  extends UserBase
    """
    organizations = List[Organization]
    collaborations = List[Collaboration]
