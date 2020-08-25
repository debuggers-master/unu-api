"""
Organizations  Schema Models
"""

from typing import List
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
    organizationId: str = Field(...,
                                description="UUID of a organization")


class OrganizationBase(BaseModel):
    """
    Base Model for organization
    """
    organizationName: str = Field(...,
                      description="name of organization",
                      example="Cosas de ingenieros")

class OrganizationIn(UserId):
    """
    Base Model for creates new organization
    """
    organizationData : OrganizationBase

class OrganizationOut(OrganizationId, OrganizationBase):
    """
    Base Model returned when a new organization is  just created
    """

class OrganizationUpdate(UserId):
    """
    Base Model to organization Update
    """
    organizationData: OrganizationOut

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
