"""
Events Router - Operations about events
"""

from fastapi import APIRouter, HTTPException

from schemas.events.events import EventIn, EventOut
from schemas.events.events import InformationIn, InformationDB
from api.v1.services.events.create import CreateEvent
from api.v1.services.events.delete import DeleteEvent
from api.v1.services.events.update import UpdateEvent

from schemas.events.collaborators import CollaboratorIn, CollaboratorOut, CollaboratorDelete, CollaboratorUpdate
from schemas.events.associates import AssociateIn, AssociateOut, AssociateDelete, AsociateUpdate
from schemas.events.speakers import SpeakerIn, SpeakerOut, SpeakerDelete, SpeakerUpdate

# Router instance
router = APIRouter()
CreateMethods = CreateEvent()
DeleteMethods = DeleteEvent()
UpdateMethods = UpdateEvent()

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


##########################
##Collaborators API CRUD##
##########################

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
    Delete  a collaborator into  a event
    using eventId and collaboratorId
    """
    await DeleteMethods.collaborators(
        event_id=collaborator.eventId,
        collaborator_id=collaborator.collaboratorId)


@router.put("/collaborator/",
            status_code=204)
async def update_collaborator(collaborator: CollaboratorUpdate):
    """
    Update a collaborator into  a event
    using eventId and collaboratorId
    """
    await UpdateMethods.collaborators(
        event_id=collaborator.eventId,
        collaborator_id=collaborator.collaboratorId,
        new_data=collaborator.collaboratorData.dict())


#######################
##ASSOCIATES API CRUD##
#######################
@router.post("/associate/",
             status_code=200,
             response_model=AssociateOut)
async def add_associate(new_associate: AssociateIn):
    """
    Add an associate to a event
    using eventId
    """

    ##base64img= new_associate.logo

    #######################
    ## URL created  Image Logic ##
    #######################

    associate = new_associate.asociateInfo.dict()
    associate.update({"url_logo": "url_logo"})

    associate_id = await CreateMethods.add_associates(
                                event_id=new_associate.eventId,
                                associate_data=associate)

    # No se de donde toma el associateId :O
    return AssociateOut(**associate)

@router.delete("/associate/",
               status_code=204)
async def delete_associate(associate: AssociateDelete):
    """
    Delete  a associate into  a event
    using eventId and associateId
    """
    await DeleteMethods.associates(
        event_id=associate.eventId,
        associate_id=associate.associateId)

@router.put("/associate/",
            status_code=200)
async def updatee_associate(associate: AsociateUpdate):
    """
    Update  a associate into  a event
    using eventId and associateId
    """


#######################
## Speakers API CRUD ##
#######################

@router.post("/speaker/",
             status_code=200,
             response_model=SpeakerOut)
async def add_speaker(new_speaker:SpeakerIn):
    """
    Add a Speaker to a event
    using eventId
    """

    ##base64img= new_associate.logo

    #######################
    ## URL created  Image Logic ##
    #######################

    associate = new_associate.asociateInfo.dict()
    associate.update({"url_logo": "url_logo"})

    associate_id = await CreateMethods.add_associates(
                                event_id=new_associate.eventId,
                                associate_data=associate)

    # No se de donde toma el associateId :O
    return AssociateOut(**associate)