"""
Events Router - Operations about events
"""

from fastapi import APIRouter, HTTPException

from schemas.events.events import EventIn, EventOut
from schemas.events.events import InformationIn, InformationDB
from api.v1.services.events.create import CreateEvent

# Router instance
router = APIRouter()
CreateMethods  = CreateEvent()

@router.get("",
            status_code=200,
            response_model=EventOut)
async def get_event(get_event: EventIn):
    """
    Get a event using eventId
    """


@router.put("",
            status_code=200,
            response_model=EventOut)
async def update_event(update_event: EventIn):
    """
    Get create a new event
    """



@router.post("",
            status_code=200,
            response_model=EventOut)
async def create_event(new_event: EventIn):
    """
    Create a new event
    """
    

    eventId = await CreateMethods.create_event(event_data=new_event.dict())

    return  eventId

@router.delete("",
            status_code=200,
            response_model=EventOut)
async def delete_event(event: EventIn):
    """
    Get create a new event 
    """


######################
##Collaborators API CRUD##
######################

@router.post("/collaborator/",
            status_code=200,
            response_model=EventOut)
async def add_collaborator(collaborator: EventIn):
    """
    Add a collaborator to a event
    using eventId
    """

# CreateMethods