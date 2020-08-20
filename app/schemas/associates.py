"""
Asocciates  Schema Models
"""

from typing import List, Optional
from pydantic import BaseModel, HttpUrl, Field  # pylint: disable-msg=E0611


class AssociateBase(BaseModel):
    """
    Base model for add associate
    """
    name: str = Field(...,
                      description="Name of associate",
                      example="Platzi")
    url: HttpUrl = Field(None,
                         description="Url Associate WebPage",
                         example="https://platzi.com")
    urlLogo: str = Field(None,
                         description="Url Logo associate")
    tag: str = Field(None,
                     description="Tag to identify asociate")


class AssociateIn(AssociateBase):
    """
    Base model for add associate
    """
    eventId: str = Field(...,
                         description="Unique Id of an event",
                         example="string")


class AssociateOut(AssociateBase):
    """
    Base model for add associate
    """
    AssociateId: str = Field(...,
                             description="Unique Id of an associate",
                             example="string")


class OrganizationDB(BaseModel):
    """
    Base model for add associate
    """
    AssociateId: str = Field(None,
                             description="Unique Id of an associate",
                             example="string")

class Associates(BaseModel):
    """
    Base model for list of associates
    """
    associates: Optional[List[OrganizationDB]] = []
