"""
Register Schema Models
"""

from pydantic import BaseModel, EmailStr, Field # pylint: disable-msg=E0611

class ResistersIn(BaseModel):
    """
    Base Model to register in events webpage
    """
    event_id: str = Field(...,
                          description="Unique Id identifier for organization")
    email: EmailStr = Field(...,
                            description="Email of new register")

class RegisterOut(BaseModel):
    """
    Base Model to register event setting
    """
    amount: int = Field(...,
                        description="Amount of mails registers so far",
                        example=" The Event App Show")
