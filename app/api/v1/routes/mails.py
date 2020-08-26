"""
Mails Router - Operations about send mails
"""

from datetime import datetime, timedelta

from pydantic import BaseModel, Field
from fastapi import (
    APIRouter, Depends, Form, UploadFile, HTTPException, BackgroundTasks, Query)

from auth.services import get_current_user
from schemas.users import UserOut
from api.v1.services.events.get import GetEvent
from mails.service import (
    send_special_email, send_welcome_email, send_close_event_email)

# Router instance
router = APIRouter()

# Service instance
events_service = GetEvent()


# Mails Schemas
class MailResponse(BaseModel):
    """
    The mail response.
    """
    detail: str = Field("Emails sended", description="De sended status")


# Exceptions
not_found_event = HTTPException(status_code=404, detail="Event Not Found")


@router.post("/special", response_model=MailResponse)
async def send_email_to_participants(
        background_task: BackgroundTasks,
        eventId: str = Form(...),
        subject: str = Form(...),
        message: str = Form(...),
        image: UploadFile = Form(None),
        current_user: UserOut = Depends(get_current_user)):
    """
    Send a message to participants with the content that the organiztors specify.
    """
    event = await events_service.get_event(
        eventId, filters=["name", "eventId", "organizationUrl", "url"])

    if not event:
        raise not_found_event

    event_name = event.get("name")
    organization_url = event.get("organizationUrl")
    url = event.get("url")
    event_url = f"{organization_url}/{url}"

    to_list = await events_service.get_particpants(eventId)

    content_type = None
    if image:
        content_type: str = image.content_type
        image: bytes = await image.read()

    # No blocking the treath with background proccess.
    background_task.add_task(
        send_special_email,
        event_name, message, subject, to_list, event_url,
        image=image, content_type=content_type)

    return MailResponse()


@router.post("/welcome", response_model=MailResponse)
async def send_welcome_email_to_user(
        background_task: BackgroundTasks,
        email: str = Query(...), name: str = Query(...)):
    """
    Send a a welcome email to new user.
    """

    background_task.add_task(send_welcome_email, name, email)
    return MailResponse()


@router.post("/alert", response_model=MailResponse)
async def send_alert_event_message_to_participants(
        background_task: BackgroundTasks, eventId: str = Query(...)):
    """
    Schedule a email to be sended to all registered participants
    one day before the event beggins.
    """
    to_list = await events_service.get_particpants(eventId)
    event = await events_service.get_event(
        eventId, filters=["name", "url", "organizationUrl", "startDate", "localTime"])

    url = event.get("url")
    organization_url = event.get("organizationUrl")
    event_url = f"{organization_url}/{url}"
    event_name = event.get("name")

    local_time: str = event.get("localTime")
    utc_hours: int = int(local_time.split("C")[1])

    start_date: str = event.get("startDate")
    # Convert 'Tue Aug 25 2020 20:32:08' -> 'Tue-Aug-25-2020-20'
    date_string = start_date.replace(" ", "-").split(":")[0]
    date_time = datetime.strptime(date_string, "%a-%b-%d-%Y-%H")
    send_at = date_time - timedelta(days=1)

    background_task.add_task(
        send_close_event_email,
        event_name,
        event_url,
        to_list,
        send_at,
        utc_hours=utc_hours
    )

    return MailResponse()
