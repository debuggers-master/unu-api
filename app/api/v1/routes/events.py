"""
Events Router - Operations about events
"""
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel

from api.v1.services.events.create import CreateEvent
from api.v1.services.events.delete import DeleteEvent
from api.v1.services.events.update import UpdateEvent
from api.v1.services.events.get import GetEvent

from auth.services import get_current_user

from schemas.users import UserOut
from schemas.events.event import NewEvent, EventOut, EventIn

# Router instance
router = APIRouter()

# Services
CreateMethods = CreateEvent()
ReadMethods = GetEvent()
DeleteMethods = DeleteEvent()
UpdateMethods = UpdateEvent()


# Response Model
class EventResponse(BaseModel):
    """
    Response class.
    """
    eventId: str


class CountParticipantsResponse(BaseModel):
    """
    Response class.
    """
    participants: int


class UpdateResponse(BaseModel):
    """
    Response class.
    """
    modifiedCount: int


# Exceptions
server_error = HTTPException(status_code=500, detail="Internal server error")
not_found = HTTPException(status_code=404, detail="Not found")


###########################################
##            Events API CRUD            ##
###########################################

@router.post("/",
             status_code=201,
             response_model=EventResponse)
async def create_event(
        new_event: NewEvent, curret_user: UserOut = Depends(get_current_user)):
    """
    Create a new event
    """
    event_id = await CreateMethods.create_event(
        new_event.dict(), curret_user.email)
    if not event_id:
        raise server_error
    return event_id


@router.get("/",
            status_code=200,
            response_model=EventOut)
async def get_event(
        eventId: str = Query(..., description="The event id"),
        filters: Optional[list] = Query(None),
        excludes: Optional[list] = Query(None)):
    """
    Get a event using eventId
    """
    event_info = await ReadMethods.get_event(
        event_id=eventId, filters=filters, excludes=excludes)
    if not event_info:
        raise not_found
    return event_info


@router.get("/from-url",
            status_code=200,
            response_model=EventOut)
async def get_event_from_url(
        organizationName: str = Query(...),
        url: str = Query(..., description="The custom event url"),
        filters: Optional[list] = Query(None),
        excludes: Optional[list] = Query(None)):
    """
    Get a event using eventId
    """
    event_info = await ReadMethods.get_event_from_url(
        organizationName, url,
        filters=filters, excludes=excludes)
    if not event_info:
        raise not_found
    return event_info


@router.get("/list",
            status_code=200,
            response_model=List[EventOut])
async def get_published_events():
    """
    Retrieve a list with all published events.
    """
    event_list = await ReadMethods.get_published_events()
    return event_list


@router.get("/count-participants",
            status_code=200,
            response_model=CountParticipantsResponse)
async def get_events_count_participants(eventId: str = Query(...)):
    """
    Return the number of registered participants to an event.
    """
    count = await ReadMethods.get_count_particpants(event_id=eventId)
    return count


@router.put("/",
            status_code=200,
            response_model=UpdateResponse)
async def update_event(update_info: EventIn):
    """
    Update a created event.
    """
    updated = await UpdateMethods.principal_info(
        event_id=update_info.eventId, new_data=update_info.eventData.dict())
    return updated


@router.delete("/", status_code=204)
async def delete_event(eventId: str = Query(...)):
    """
    Delete a existing event
    """
    deleted = await DeleteMethods.all(event_id=eventId)
    if not deleted:
        raise not_found
    return


###########################################
##     Events/Collaborators API CRUD     ##
###########################################

# @router.post("/collaborator/",
#              status_code=200,
#             response_model=CollaboratorOut)
# async def add_collaborator(new_collaborator: CollaboratorIn):
#     """
#     Add a collaborator to a event
#     using eventId
#     """
#     collaborator_id = await CreateMethods.add_collaborator(event_id=new_collaborator.eventId,
#                                                           collaborator_data=new_collaborator.collaboratorInfo.dict())
#     if collaborator_id is  False:
#         raise HTTPException(status_code=500,
#                             detail="Error Adding Collaborator, Maybe EventId is Wrong")
#     return collaborator_id
# @router.delete("/collaborator/",
#                status_code=204)
# async def delete_collaborator(collaborator: CollaboratorDelete):
#     """
#     Delete  a collaborator into  a event
#     using eventId and collaboratorId
#     """
#     await DeleteMethods.collaborators(
#         event_id=collaborator.eventId,
#         collaborator_id=collaborator.collaboratorId)
# @router.put("/collaborator/",
#             status_code=204)
# async def update_collaborator(collaborator: CollaboratorUpdate):
#     """
#     Update a collaborator into  a event
#     using eventId and collaboratorId
#     """
#     await UpdateMethods.collaborators(
#         event_id=collaborator.eventId,
#         collaborator_id=collaborator.collaboratorId,
#         new_data=collaborator.collaboratorData.dict())
# #######################
# ##ASSOCIATES API CRUD##
# #######################
# @router.post("/associate/",
#              status_code=201,
#              response_model=AssociateOut)
# async def add_associate(new_associate: AssociateIn):
#     """
#     Add an associate to a event
#     using eventId
#     """
#     ##base64img= new_associate.logo
#     #######################
#     ## URL created  Image Logic ##
#     #######################
#     associate = new_associate.asociateInfo.dict()
#     associate.update({"url_logo": "url_logo"})
#     associate_id = await CreateMethods.add_associates(
#                                 event_id=new_associate.eventId,
#                                 associate_data=associate)
#     # No se de donde toma el associateId :O
#     return AssociateOut(**associate)
# @router.delete("/associate/",
#                status_code=204)
# async def delete_associate(associate: AssociateDelete):
#     """
#     Delete  a associate into  a event
#     using eventId and associateId
#     """
#     await DeleteMethods.associates(
#         event_id=associate.eventId,
#         associate_id=associate.associateId)
# @router.put("/associate/",
#             status_code=200)
# async def updatee_associate(associate: AsociateUpdate):
#     """
#     Update  a associate into  a event
#     using eventId and associateId
#     """
# #######################
# ## Speakers API CRUD ##
# #######################
# @router.post("/speaker/",
#              status_code=200,
#              response_model=SpeakerOut)
# async def add_speaker(new_speaker:SpeakerIn):
#     """
#     Add a Speaker to a event
#     using eventId
#     """
#     ##base64img= new_associate.logo
#     ##############################
#     ## URL created  Image Logic ##
#     ##############################
#     speaker = new_speaker.spekerInfo.dict()
#     speaker.update({"url_photo": "url_photo"})
#     speaker_id = await CreateMethods.add_speaker(
#                             event_id=new_speaker.eventId,
#                             speaker_data=new_speaker.spekerInfo)
#     # No se de donde toma el associateId :O
#     return AssociateOut(**associate)
