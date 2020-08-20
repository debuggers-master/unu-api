"""
User Schema Models
"""
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field  # pylint: disable-msg=E0611

from .organizations import OrganizationDB
from .collaborations import CollaborationOut


class UserBase(BaseModel):
    """
    Base Model for user, and user update
    """
    firstName: str = Field(None,
                           description="Name of user",
                           example="Mario")
    lastName: str = Field(None,
                          description="Lastname of user",
                          example="Barbosa")


class UserIn(UserBase):
    """
    Base Model for register new user , this class extends UserBase
    """
    email: EmailStr = Field(...,
                            description="Email of user",
                            example="name_last@organization.com")
    password: str = Field(...,
                          description="Password of user account")


class UserOut(UserBase):
    """
    Base Model returned when user is login new, this class  extends UserBase
    """
    userID: str = Field(...,
                        description="Unique uuid identifier")
    organizations: Optional[List[OrganizationDB]] = []
    collaborations: Optional[List[CollaborationOut]] = []
