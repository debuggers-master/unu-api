"""
Collaboratos Schema Models
"""

from pydantic import BaseModel

from schemas.users import UserBase 


class CollaboratosIn(UserBase):
    