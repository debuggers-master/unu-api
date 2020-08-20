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
                             example="Comunidad para  enseñar a los ingenieros del futuro")

class OrganizationIn(OrganizationBase):
    """
    Base Model for creates new organization
    """
    ownerId: str = Field(...,
                         description="UserId of the owner",
                         example="string")

class OrganizationDB(OrganizationBase):
    """
    Base Model upload to DB when organization
    is created  and give back when user is logged
    """
    organizationId: str = Field(None,
                                description="Unique Id of organization")

class OrganizationOut(BaseModel):
    """
    Base Model returned when a new organization is  just created
    """
    organizationId: str = Field(...,
                                description="Unique Id of organization")
