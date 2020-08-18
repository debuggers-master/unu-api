"""
Events Schema Models
"""

from enum import Enum
from pydantic import BaseModel, HttpUrl, Field # pylint: disable-msg=E0611

class Templates(str, Enum):
    """
        Template choice list
    """
    template1 = "template1"
    template2 = "template2"

class EventIn(BaseModel):
    """
    Base Model for create a event
    """
    name: str = Field(...,
                      description="Name of event",
                      example="Python Week Code")
    organization_id: str = Field(...,
                                 description="Email of user",
                                 example="name_last@organization.com")
    url: str = Field(...,
                     description="event url identifier",
                     example="cosas-de-inges/py-week")
    startDate: str = Field(...,
                           description="Date of Start of event",
                           example="28/08/2020")
    template: Templates

class Information(BaseModel):
    """
    Base Model for aditional event settings
    """
    startHour: str = Field(...,
                           description="Hour at the event start 24H format",
                           example="16:00")
    timeZone: str = Field(...,
                          description="UTC of event strat hour",
                          example="-5 UTC")
    localization: str = Field(...,
                              description="Localization of event",
                              example="Online")

class Banner(BaseModel):
    """"
    Base Model for edit Banner
    """
    title: str = Field(...,
                       description="Title of event to show in banner",
                       example="Python week code colombia")
    urlImg: HttpUrl = Field(...,
                            description="url of banner image")
    dateBanner: str = Field(None,
                            description="url of banner image",
                            example="28, 29 and 30 of agust")
