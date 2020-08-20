"""
Events Schema Models
"""

from enum import Enum
from pydantic import BaseModel, HttpUrl, Field  # pylint: disable-msg=E0611


class Templates(str, Enum):
    """
    Template choice list
    """
    template1 = "template1"
    template2 = "template2"


class MinInfo(BaseModel):
    """
    Base Model for create a new event
    """
    name: str = Field(...,
                      description="Name of event",
                      example="Python Week Code")
    startDate: str = Field(...,
                           description="Date of Start of event",
                           example="28/08/2020")
    template: Templates
    url: str = Field(...,
                     description="event url contex",
                     example="py-week")
    organizationId: str = Field(...,
                                description="Unique ID of an organization",
                                example="string")
    description: str = Field(None,
                             description="Unique ID of an organization",
                             example="string")
    shortDescription: str = Field(None,
                                  description="Unique ID of an organization",
                                  example="string")

class EventOut(BaseModel):
    """
    Base Model returned when a new event is just  created
    """
    eventId: str = Field(...,
                         description="Unique Id of an event")

class EventDelete(EventOut):
    """
    Base Model for delete and event
    """


class InformationDB(BaseModel):
    """
    Base Model for aditional event settings
    """
    timeZone: str = Field(None,
                          description="UTC of event strat hour",
                          example="-5 UTC")
    localization: str = Field(None,
                              description="Localization of event",
                              example="Online")


class Banner(BaseModel):
    """"
    Base Model for edit Banner
    """
    title: str = Field(None,
                       description="Title of event to show in banner",
                       example="Python week code colombia")
    urlImg: HttpUrl = Field(None,
                            description="url of banner image")
    dateBanner: str = Field(None,
                            description="url of banner image",
                            example="28, 29 and 30 of agust")
