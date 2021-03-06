"""
Events Router - Operations about events
"""

from typing import List, Optional
from datetime import datetime, timedelta
import requests

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel  # pylint: disable-msg=E0611

from config import settings  # pylint: disable-msg=E0611
from api.v1.services.events.create import CreateEvent
from api.v1.services.events.delete import DeleteEvent
from api.v1.services.events.update import UpdateEvent
from api.v1.services.events.get import GetEvent

from worker.main import create_job
from auth.services import get_current_user

from schemas.users import UserOut
from schemas.events.associates import (
    AssociatedIn, AssociatedUpdate, AssociatedOnDelete)
from schemas.events.event import NewEvent, EventOut, EventIn, EventPublishOut
from schemas.events.collaborators import NewCollaborator, CollaboratorOnDelete
from schemas.events.agenda import DayIn, DayUpdate, DayOnDelete
from schemas.events.agenda import (
    ConferenceIn, ConferenceUpdate, ConferenceOnDelete)


###########################################
##            Router Instance            ##
###########################################

router = APIRouter()

###########################################
##            Events Services            ##
###########################################

CreateMethods = CreateEvent()
ReadMethods = GetEvent()
DeleteMethods = DeleteEvent()
UpdateMethods = UpdateEvent()


###########################################
##                   Models              ##
###########################################
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


class DayResponse(BaseModel):
    """
    Response class.
    """
    dayId: str


class ConferenceResponse(BaseModel):
    """
    Response class.
    """
    conferenceId: str
    speakerId: str


###########################################
##               Exceptions              ##
###########################################

server_error = HTTPException(status_code=500, detail="Internal server error")
not_found = HTTPException(status_code=404, detail="Not found")
conflict_request = HTTPException(
    status_code=409, detail="The user already exists")


###########################################
##            Events API CRUD            ##
###########################################

@router.post(
    "/",
    status_code=201,
    response_model=EventResponse)
async def create_event(
        new_event: NewEvent,
        curret_user: UserOut = Depends(get_current_user)):
    """
    Create a new event
    """
    event_id = await CreateMethods.create_event(
        new_event.dict(), curret_user.email)

    if event_id == 409:
        raise HTTPException(status_code=409,
                            detail="url event is already used")

    if not event_id:
        raise server_error
    return event_id


@router.get(
    "/",
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


@router.get(
    "/from-url",
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

    organization_url = organizationName.lower()

    event_info = await ReadMethods.get_event_from_url(
        organization_url, url,
        filters=filters, excludes=excludes)

    if not event_info:
        raise not_found
    return event_info


@router.get(
    "/list",
    status_code=200,
    response_model=List[EventPublishOut])
async def get_published_events():
    """
    Retrieve a list with all published events.
    """
    event_list = await ReadMethods.get_published_events()
    return event_list


@router.get(
    "/count-participants",
    status_code=200,
    response_model=CountParticipantsResponse)
async def get_events_count_participants(eventId: str = Query(...)):
    """
    Return the number of registered participants to an event.
    """
    count = await ReadMethods.get_count_particpants(event_id=eventId)
    return count


@router.put(
    "/",
    status_code=200,
    response_model=UpdateResponse)
async def update_event(
        update_info: EventIn,
        curret_user: UserOut = Depends(get_current_user)):
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


###########################################
##     Events/Collaborators API CRUD     ##
###########################################

@router.post(
    "/collaborators",
    status_code=200,
    response_model=CollaboratorResponse)
async def add_collaborator(
        info: NewCollaborator,
        existing: Optional[bool] = Query(False),
        curret_user: UserOut = Depends(get_current_user)):
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


@router.delete("/collaborators", status_code=204)
async def delete_collaborator(
        body: CollaboratorOnDelete,
        curret_user: UserOut = Depends(get_current_user)):
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


@router.post("/associates", status_code=201, response_model=AssociatedResponse)
async def add_associated(
        body: AssociatedIn,
        curret_user: UserOut = Depends(get_current_user)):
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


@router.put("/associates", status_code=200, response_model=UpdateResponse)
async def update_associated(
        body: AssociatedUpdate,
        curret_user: UserOut = Depends(get_current_user)):
    """
    Update an existing associated.
    """

    modified_status = await UpdateMethods.associateds(
        event_id=body.eventId,
        associated_id=body.associatedData.associatedId,
        new_data=body.associatedData.dict())

    return modified_status


@router.delete("/associates", status_code=204)
async def delete_associate(
        body: AssociatedOnDelete,
        curret_user: UserOut = Depends(get_current_user)):
    """
    Delete  a associate into  a event
    using eventId and associateId
    """
    await DeleteMethods.associates(
        event_id=body.eventId,
        associate_id=body.associatedId)


###########################################
##          Events/day API CRUD          ##
###########################################

@router.post("/day", status_code=201, response_model=DayResponse)
async def create_day(
        body: DayIn, curret_user: UserOut = Depends(get_current_user)):
    """
    Add a new day to agenda.
    """
    day_id = await CreateMethods.add_day(
        event_id=body.eventId, day_data=body.dayData.dict())

    if not day_id:
        raise HTTPException(status_code=409, detail="The date is used")
    return day_id


@router.put("/day", status_code=200, response_model=UpdateResponse)
async def update_day(
        body: DayUpdate, curret_user: UserOut = Depends(get_current_user)):
    """
    Update a existing day in agenda.
    """
    day_id = await UpdateMethods.days(
        event_id=body.eventId, day_data=body.dayData.dict())

    if not day_id:
        raise HTTPException(status_code=409, detail="The date is used")
    return day_id


@router.delete("/day", status_code=204)
async def delete_day(
        body: DayOnDelete, curret_user: UserOut = Depends(get_current_user)):
    """
    Delete a existing day in agenda.
    """
    await DeleteMethods.days(
        event_id=body.eventId, day_id=body.dayId)
    return


###########################################
##      Events/conferences API CRUD      ##
###########################################

@router.post("/conference", status_code=201, response_model=ConferenceResponse)
async def create_a_conference(
        body: ConferenceIn, curret_user: UserOut = Depends(get_current_user)):
    """
    Create a new conference.
    """
    conference_response = await CreateMethods.add_conference(
        event_id=body.eventId,
        day_id=body.dayId,
        conference_data=body.conferenceData.dict())

    if not conference_response:
        raise not_found
    return conference_response


@router.put("/conference", status_code=200, response_model=UpdateResponse)
async def update_a_conference(
        body: ConferenceUpdate,
        curret_user: UserOut = Depends(get_current_user)):
    """
    Update a existing conference.
    """
    conference_response = await UpdateMethods.conference(
        event_id=body.eventId,
        day_id=body.dayId,
        conference_data=body.conferenceData.dict())

    return conference_response


@router.delete("/conference", status_code=200)
async def delete_a_conference(
        body: ConferenceOnDelete,
        curret_user: UserOut = Depends(get_current_user)):
    """
    Delete a existing conference.
    """
    await DeleteMethods.conference(
        event_id=body.eventId,
        day_id=body.dayId,
        conference_id=body.conferenceId,
        speaker_id=body.speakerId)

    return


###########################################
##       Events/change-status API        ##
###########################################

@router.put("/change-status", status_code=200, response_model=dict)
async def change_publication_status(
        actualStatus: bool,
        eventId: str,
        current_user: UserOut = Depends(get_current_user)):
    """
    Change the publication status of the event.
    """
    response = await UpdateMethods.change_status(
        eventId, actualStatus, current_user.email)
    if response == 403:
        raise HTTPException(status_code=403, detail="Operation Forbbiden")

    # Schedule email to participats one day before the event
    event = await ReadMethods.get_event(eventId)
    local_time: str = event.get("localTime")
    utc_hours: int = int(local_time.split("C")[1])
    start_date: str = event.get("startDate")

    # Convert 'Tue Aug 25 2020 20:32:08' -> 'Tue-Aug-25-2020-20'
    date_string = start_date.replace(" ", "-").split(":")[0]
    date_time = datetime.strptime(date_string, "%a-%b-%d-%Y-%H")
    send_at = date_time - timedelta(days=1)

    url = f"{settings.HOST}/api/v1/mails/alert?eventId={eventId}"
    create_job(requests.post, date_time=send_at, utc_hours=utc_hours, url=url)

    return response
