"""
Associates schema Models
"""
from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field

from schemas.events.events  import EventOut

class Tag(str, Enum):
    """
    Template choice list
    """
    sponsor = "sponsor"
    community = "community"


class AsociateInfo(BaseModel):
    """
    Base Model to add Associate
    """
    name: str = Field(None,
                      description="Name of Associate",
                      example="Platzi")
    website: str = Field(None,
                         description="Web page of associate",
                         example="platzi.com")
    tag: Optional[Tag]


class AssociateIn(EventOut):
    """
    Base Model to add Associate
    """
    asociateInfo: AsociateInfo
    logo: str = Field(None,
                      description="Image of associate in base64")


class AssociateOut(BaseModel):
    """
    Base Model returned when a new associate is just added
    """
    associateId: str = Field(...,
                             description="Unique Associate uuid identifier")
    url_logo: str = Field(None,
                          description="url of associate logo")

class AssociateDelete(EventOut,AssociateOut):
    """
    Base Model to delele a associate
    """


class AsociateUpdate(AssociateDelete):
    """
    Base Model to Update a associate
    """
    asociateInfo: Optional[AsociateInfo]