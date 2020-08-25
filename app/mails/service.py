"""
Functions to manage the SendGrid Sender.
"""
from typing import List
from datetime import datetime
from fastapi import UploadFile

from mails.templates.welcome import welcome_template
from mails.templates.event_close import event_close_template
from mails.templates.special_message import special_message_template
from .sender import EmailSender

# SendGrid sender abstraction.
sender = EmailSender()


# ----------------------- Email functions ---------------------- #

def send_welcome_email(username: str, email: str) -> None:
    """
    Send a welcome email.

    Params:
    ------
    username: str - The username of the new user
    email: str - The target email
    """
    content = welcome_template(name=username)
    email = sender.create_email(
        to_list=[email],
        subject=f"Unu app - Bienvenido {username}",
        html_content=content,
    )
    sender.send_email(email_to_send=email)


def send_special_email(
        event_name: str,
        message: str,
        subjet: str,
        to_list: List[str],
        image: UploadFile = None,
        send_at: datetime = None
) -> None:
    """
    Send a special email.

    Params:
    ------
    event_name: str - The event name.
    message: str - The message to participants.
    subject: str - The email sibject.
    to_list: List[str] - The participants emails.
    send_at: datetime - Optional date to send the mail.
    """
    content = special_message_template(event_name, message)
    email = sender.create_email(
        to_list=to_list,
        subject=subjet,
        html_content=content,
        send_at=send_at,
    )
    sender.send_email(email_to_send=email)


def send_close_event_email(
        event_name: str,
        event_url: str,
        to_list: List[str],
        send_at: datetime,
) -> None:
    """
    Send a schedule email to notify that a event is tomorrow.

    Params:
    ------
    event_name: str - The event name.
    event_url: str - The public event url.
    to_list: List[str] - The participants emails.
    send_at: datetime - The date to send the mail.
    """
    content = event_close_template(event_name, event_url)
    email = sender.create_email(
        to_list=to_list,
        subject="Unu Events - Notificación =)",
        html_content=content,
        send_at=send_at,
    )
    sender.send_email(email_to_send=email)