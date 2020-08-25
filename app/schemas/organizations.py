"""
Organizations  Schema Models
"""

from typing import List, Optional
from pydantic import BaseModel, Field  # pylint: disable-msg=E0611

class Events(BaseModel):
    """
    Base Model for request or return eventId
    """
    eventId: str = Field(...,
                         description="UUID of a event")
    name: str = Field(...,
                    description="Name of event",
                    example="Python Week Code")


class OrganizationId(BaseModel):
    """
    Base Model for request or return organizationId
    """
    organizationId: str = Field(...,
                                description="UUID of a event")

class OrganizationBase(BaseModel):
    """
    Base Model for organization
    """
    name: str = Field(...,
                      description="name of organization",
                      example="Cosas de ingenieros")

class OrganizationIn(OrganizationBase):
    """
    Base Model for creates new organization
    """
    userIdOwner: str = Field(...,
                             description="The user Id of owner of organization",)


class OrganizationOut(OrganizationBase):
    """
    Base Model returned when a new organization is  just created
    """
    organizationId: str = Field(None,
                                description="Unique Id for organization")
    events: Optional[List[Events]] = []


class OrganizationDelete(BaseModel):
    """
    Base Model for delete and organization
    """
    organizationId: str = Field(...,
                                description="Unique Id for organization")
    userIdOwner: str = Field(...,
                             description="The user Id of owner of organization",)

class OrganizationUpdate(OrganizationDelete):
    """
    Base Model for update  and organization
    """
    name: str = Field(...,
                      description="name of organization",
                      example="Cosas de ingenieros")
