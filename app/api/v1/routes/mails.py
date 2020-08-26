"""
Mails Router - Operations about send mails
"""

from typing import Optional
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
    event = await events_service.get_event(eventId, filters=["name", "eventId"])
    if not event:
        raise not_found_event

    event_name = event.get("name")
    to_list = await events_service.get_particpants(eventId)

    if image:
        image = await image.read()
    background_task.add_task(
        send_welcome_email, "Emanuel", ["emanuelosva@gmail.com"])
    #event_name, message, subject, to_list, image=image
    return MailResponse()
