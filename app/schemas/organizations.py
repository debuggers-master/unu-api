"""
Organizations  Schema Models
"""

from pydantic import BaseModel, Field  # pylint: disable-msg=E0611


class OrganizationIn(BaseModel):
    """
    Base Model for creates new organization
    """
    name: str = Field(...,
                      description="name of organization",
                      example="Cosas de ingenieros")
    url: str = Field(...,
                     description="organization url identifier",
                     example="cosas-de-inges")
    ownerEmail: str = Field(...,
                            description="email registered by the user owner of organization",
                            example="mariobarbosa777@hotmail.com")

class OrganizationOut(BaseModel):
    """
    Base Model returned when a new organization is created
    """
    organization_id: str = Field(...,
                                 description="Unique Id for organization")
