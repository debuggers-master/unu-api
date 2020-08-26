"""
General Usse  Schema Models
"""

from pydantic import BaseModel, Field  # pylint: disable-msg=E0611


class ModifiedCount(BaseModel):
    """
    Base Model for modifiedCount
    used in updates methods
    """
    modifiedCount: str = Field(...,
                               description="Modified values in update",
                               example="1")

class ModifiedCountUrls(ModifiedCount):
    """
    Base Model for modifiedCount
    used in updates methods with img
    """
    url: dict = Field(None,
                      description="Modified values in update")
