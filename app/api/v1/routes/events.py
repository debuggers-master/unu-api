"""
Events Router - Operations about events
"""

from fastapi import APIRouter, HTTPException

from schemas.events.events import EventIn, EventOut
from schemas.events.events import InformationIn, InformationDB
from api.v1.services.events.create import CreateEvent
from api.v1.services.events.delete import DeleteEvent

from schemas.events.collaborators import CollaboratorIn, CollaboratorOut, CollaboratorDelete

# Router instance
router = APIRouter()
CreateMethods = CreateEvent()
DeleteMethods = DeleteEvent() 

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
    Update a create event
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
               status_code=200)
async def delete_event(event: EventIn):
    """
    Get create a new event 
    """


######################
##Collaborators API CRUD##
######################

@router.post("/collaborator/",
            status_code=200,
            response_model=CollaboratorOut)
async def add_collaborator(new_collaborator: CollaboratorIn):
    """
    Add a collaborator to a event
    using eventId
    """
    collaborator_id = await CreateMethods.add_collaborator(event_id=new_collaborator.eventId,
                                                          collaborator_data=new_collaborator.collaboratorInfo.dict())
    if collaborator_id is  False:
        raise HTTPException(status_code=500,
                            detail="Error Adding Collaborator, Maybe EventId is Wrong")

    return collaborator_id

@router.delete("/collaborator/",
            status_code=204)
async def delete_collaborator(collaborator: CollaboratorDelete):
    """
    Add a collaborator to a event
    using eventId
    """

    deleted = await DeleteMethods.collaborators(event_id=collaborator.eventId,
                                                collaborator_id=collaborator.collaboratorId)

    print(deleted)



# CreateMethods