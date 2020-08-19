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
    url: str = Field(...,
                     description="organization url identifier",
                     example="cosas-de-inges")

class OrganizationIn(OrganizationBase):
    """
    Base Model for creates new organization
    """
    ownerEmail: str = Field(...,
                            description="email registered by the user owner of organization",
                            example="mariobarbosa777@hotmail.com")

class OrganizationDB(OrganizationBase):
    """
    Base Model upload to DB when organization
    is created  and give back when user is logged
    """
    organization_id: str = Field(None,
                                 description="Unique Id for organization")

class OrganizationOut(BaseModel):
    """
    Base Model returned when a new organization is  just created
    """
    organization_id: str = Field(...,
                                 description="Unique Id for organization")