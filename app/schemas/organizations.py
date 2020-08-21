"""
Organizations  Schema Models
"""

from pydantic import BaseModel, Field  # pylint: disable-msg=E0611


class OrganizationBase(BaseModel):
    """
    Base Model for organization
    """
    name: str = Field(...,
                      description="name of organization",
                      example="Cosas de ingenieros")
    description: str = Field(None,
                             description="description of organization",
                             example="Comunidad para ingenieros")


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
