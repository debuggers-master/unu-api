"""
User Schema Models
"""
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field  # pylint: disable-msg=E0611

from .organizations import OrganizationDB
from .collaborations import CollaborationOut


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


class UserOut(UserBase):
    """
    Base Model returned when user is login new, this class  extends UserBase
    """
    userId: str = Field(None, description="Unique uuid identifier")
    organizations: Optional[List[OrganizationDB]] = []
    collaborations: Optional[List[CollaborationOut]] = []
