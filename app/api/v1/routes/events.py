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
from schemas.events.associates import AssociatedIn, AssociatedUpdate, AssociatedOnDelete
from schemas.events.event import NewEvent, EventOut, EventIn
from schemas.events.collaborators import NewCollaborator, CollaboratorOnDelete

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


class CollaboratorResponse(BaseModel):
    """
    Response class.
    """
    collaboratorId: str


class AssociatedResponse(BaseModel):
    """
    Response class.
    """
    associatedId: str


# Exceptions
server_error = HTTPException(status_code=500, detail="Internal server error")
not_found = HTTPException(status_code=404, detail="Not found")
conflict_request = HTTPException(
    status_code=409, detail="The user already exists")


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
async def delete_event(
        eventId: str = Query(...),
        current_user: UserOut = Depends(get_current_user)):
    """
    Delete a existing event
    """
    deleted = await DeleteMethods.all(eventId, current_user.email)
    if not deleted:
        raise not_found
    return


###########################################
##     Events/Collaborators API CRUD     ##
###########################################

@router.post("/collaborators",
             status_code=200,
             response_model=CollaboratorResponse)
async def add_collaborator(
        info: NewCollaborator,
        existing: Optional[bool] = Query(False)):
    """
    Add a collaborator to a event
    using eventId
    """
    if existing:
        result = await CreateMethods.add_existing_collaborator(
            event_id=info.eventId, email=info.email)
    else:
        result = await CreateMethods.add_collaborator(
            event_id=info.eventId,
            collaborator_data=info.collaboratorData)

    if result == 404:
        raise not_found
    if result == 409:
        raise conflict_request
    if result == 412:
        raise HTTPException(status_code=412, detail="The user must be created")
    return result


@router.delete("/collaborators",
               status_code=204)
async def delete_collaborator(body: CollaboratorOnDelete):
    """
    Delete  a collaborator.
    """
    deleted = await DeleteMethods.collaborators(
        event_id=body.eventId, collaborator_email=body.email)

    if not deleted:
        raise not_found
    return


###########################################
##      Events/Associateds API CRUD      ##
###########################################


@router.post("/associates",
             status_code=201,
             response_model=AssociatedResponse)
async def add_associated(body: AssociatedIn):
    """
    Add an associate to a event
    using eventId
    """

    associated_id = await CreateMethods.add_associates(
        event_id=body.eventId,
        associated_data=body.associatedData.dict())

    if not associated_id:
        raise not_found
    return associated_id


@router.put("/associates",
            status_code=200,
            response_model=UpdateResponse)
async def update_associated(body: AssociatedUpdate):
    """
    Update an existing associated.
    """

    modified_status = await UpdateMethods.associateds(
        event_id=body.eventId,
        associated_id=body.associatedData.associatedId,
        new_data=body.associatedData.dict())

    return modified_status


@router.delete("/associates",
               status_code=204)
async def delete_associate(body: AssociatedOnDelete):
    """
    Delete  a associate into  a event
    using eventId and associateId
    """
    await DeleteMethods.associates(
        event_id=body.eventId,
        associate_id=body.associatedId)

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
