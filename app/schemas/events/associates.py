"""
Associates schema Models
"""

from pydantic import BaseModel, Field  # pylint: disable-msg=E0611


class EventId(BaseModel):
    """
    Base Model for request or return eventId.
    """
    eventId: str = Field(..., description="UUID of a event")


class AssociatedInfo(BaseModel):
    """
    Base Model associated principal info.
    """
    name: str = Field(
        None,
        description="Name of Associate",
        example="Platzi")

    url: str = Field(
        None,
        description="Web page of associate",
        example="platzi.com")

    logo: str = Field(
        None,
        description="encoded base64 image")


class AssociatedInDb(AssociatedInfo):
    """
    Base Model to store Associated in db.
    """
    associatedId: str = Field(..., description="The associated uuid")


class AssociatedIn(EventId):
    """
    Base Model of request body to add a Associated.
    """
    associatedData: AssociatedInfo


class AssociatedUpdate(EventId):
    """
    Base Model of request body to update a Associated.
    """
    associatedData: AssociatedInDb


class AssociatedOnDelete(EventId):
    """
    Base Model of request body to delete a Associated.
    """
    associatedId: str = Field(..., description="The associated uuid")
