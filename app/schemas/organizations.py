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


class UserId(BaseModel):
    """
    Base Model for request or return organizationId
    """
    userId: str = Field(...,
                        description="UUID of a user")


class OrganizationId(BaseModel):
    """
    Base Model for request or return organizationId
    """
    organizationId: str = Field(None,
                                description="UUID of a organization")


class OrganizationImg(BaseModel):
    """
    BaseModel for organizationLogo
    """
    organizationLogo: Optional[str]


class OrganizationBase(OrganizationImg):
    """
    Base Model for organization Base
    """
    organizationName: str = Field(...,
                                  description="name of organization",
                                  example="Cosas de ingenieros")


class OrganizationIn(UserId):
    """
    Base Model for creates new organization
    """
    organizationData: OrganizationBase


class OrganizationOut(OrganizationId):
    """
    Base Model returned when a new organization is  just created
    """
    organizationName: str = Field(...,
                                  description="name of organization",
                                  example="Cosas de ingenieros")


class OrganizationBaseUpdate(OrganizationBase, OrganizationId):
    """
    Base Model to update a Organization
    """


class OrganizationUpdate(UserId):
    """
    Base Model to organization Update
    """
    organizationData: OrganizationBaseUpdate


class OrganizationDelete(OrganizationId, UserId):
    """
    Base Model for delete and organization
    """


class OrganizationGet(OrganizationId, OrganizationBase):
    """
    Base model returned from DB
    """
    organizationUrl: str = Field(None,
                                 description="Organization url formed by the name")
    events: List[Events]
