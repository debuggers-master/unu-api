"""
Associates schema Models
"""
from typing import Optional
from pydantic import BaseModel, Field


class EventId(BaseModel):
    """
    Base Model for request or return eventId
    """
    eventId: str = Field(...,
                         description="UUID of a event")


class AsociateInfo(BaseModel):
    """
    Base Model to add Associate
    """
    name: str = Field(None,
                      description="Name of Associate",
                      example="Platzi")
    url: str = Field(None,
                         description="Web page of associate",
                         example="platzi.com")


class AsociateImg(BaseModel):
    """
    Base Model to get str base64 for Asociate logo
    """
    logo: str = Field(None,
                      description="encoded base64 image")


class AsociateIn(AsociateInfo, AsociateImg):
    """
    Base Model to add a new Asociate
    """


class AsociateDB(AsociateInfo):
    """
    Base Model to add speaker
    """
    urlAsociateLogo : str = Field(None,
                                  description="url of speakerPhoto updloaded to the storage")
    associatedId: str = Field(...,
                              description="UUID of a speaker")
    