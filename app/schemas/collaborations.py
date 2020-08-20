"""
Organizations  Schema Models
"""
from pydantic import EmailStr, BaseModel, Field  # pylint: disable-msg=E0611


class CollaborationIn(BaseModel):
    """
    Base Model to add  collaborator in events settings
    """
    email: EmailStr = Field(...,
                            description="Email of collaborator",
                            example="Valec@gmail.com")
    firstName: str = Field(None,
                           description="first name of user",
                           example="Mario")
    lastName: str = Field(None,
                          description="Lastname of user",
                          example="Barbosa")
    eventID: str = Field(...,
                         description="Unique ID of an event")


class CollaborationOut(BaseModel):
    """
    Base Model for collaboration dictionary  when user are just login
    """
    collaboratorId: str = Field(...,
                                description="Unique ID of a collaborator")
