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
    name: str = Field(...,
                      description="Name of collaborator",
                      example="Valentina Collazos")


class CollaborationOut(BaseModel):
    """
    Base Model for collaboration dictionary  when user are just login
    """
    event_id: str = Field(...,
                          description="Unique Id identifier for organization")
    url: str = Field(...,
                     description="event url identifier",
                     example="cosas-de-inges/py-week")
    name: str = Field(...,
                      description="event name identifier",
                      example="Python code Week")
