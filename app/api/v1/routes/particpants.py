"""
Participants Router - Operations about participants
"""

from fastapi import APIRouter
from pydantic import BaseModel, Field  # pylint: disable-msg=E0611

from api.v1.services.participants import ParticipantsServices

###########################################
##            Router Instance            ##
###########################################

router = APIRouter()


###########################################
##         User Service Instance         ##
###########################################

ParticipantsMethods = ParticipantsServices()


###########################################
##                Models                 ##
###########################################
class Regiter(BaseModel):
    """
    Body request for register a user
    """
    eventId: str = Field(..., description="The event id")
    email: str = Field(..., description="Th participant email")


class RegisterResponse(BaseModel):
    """
    Body request for register a user
    """
    registered: bool


############################################
##      Participants API Endpoints        ##
############################################

@router.post("", status_code=201, response_model=RegisterResponse)
async def pregister_a_participant_to_a_event(body: Regiter):
    """
    Regiter a participant to an event.
    """
    res = await ParticipantsMethods.register(body.eventId, body.email)
    return res
