"""
Mails Router - Operations about send mails
"""

from pydantic import BaseModel, Field
from fastapi import (
    APIRouter, Depends, Form, UploadFile, HTTPException, BackgroundTasks)

from auth.services import get_current_user
from schemas.users import UserOut
from api.v1.services.events.get import GetEvent
from mails.service import send_special_email, send_welcome_email

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


@router.post("/", response_model=MailResponse)
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
        image: bytes = await image.read()
        content_type: str = image.content_type

    # No blocking the treath with background proccess.
    background_task.add_task(
        send_special_email,
        event_name, message, subject, to_list, event_url,
        image=image, content_type=content_type)

    return MailResponse()
