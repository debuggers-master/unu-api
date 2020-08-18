"""
Asocciates  Schema Models
"""

from typing import List
from pydantic import BaseModel, HttpUrl, Field  # pylint: disable-msg=E0611


class Associate(BaseModel):
    """
    Base model for add and Edit associate
    """
    name: str = Field(...,
                      description="Name of associate",
                      example="Platzi")
    url: HttpUrl = Field(...,
                         description="Url Associate WebPage",
                         example="https://platzi.com")
    urlLogo: str = Field(...,
                         description="Url Logo associate")
    tag: str = Field(None,
                     description="Tag to identify asociate")


class Associates(BaseModel):
    """
    Base model for list of associates
    """
    associates: List[Associate]
