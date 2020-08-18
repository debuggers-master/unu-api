"""
Organizations  Schema Models
"""

from pydantic import BaseModel, Field # pylint: disable-msg=E0611

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
    user_id: str = Field(...,
                         description="Unique Id for organization")

class OrganizationOut(OrganizationIn):
    """
    Base Model for organization dictionary  when user are just login
    """
    organization_id: str = Field(...,
                                 description="Unique Id for organization")
