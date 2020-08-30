"""
Emails sender class - Sendgrid implementation.
"""


import time
from datetime import datetime
from typing import List

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, From, To, Subject, SendAt,
    Content, MimeType, Attachment, FileContent,
    FileName, FileType, Disposition
)

from config import settings  # pylint: disable-msg=E0611


###########################################
##       Email Sender Abstraction        ##
###########################################

class EmailSender:
    """
    Email sender abstraction.
    """

    def __init__(self):
        self.sendgrid = SendGridAPIClient(settings.SENDGRID_API_KEY)
        self.from_email = settings.EMAIL_SENDER

    def create_email(
            self,
            to_list: List["str"],
            subject: str,
            html_content: str,
            image: bytes = None,
            content_type: str = None,
            send_at: datetime = None,
    ) -> Mail:
        """
        Create a new sendgrid email object.

        Params:
        ------
        to_list: List[str] - The recipients list.
        subject: str - The email subject.
        html_contentet: str - HTML text to fill the email.
        image: bytes - A optional image to attachment in email.
        content_type: str - The content type of the image.
        send_at: datetime - The datetime when the email must be sended.

        Return:
        ------
        message: Mail - The sendgrid email object.
        """
        message = Mail()
        message.from_email = From(self.from_email)
        message.subject = Subject(subject)

        _users_list = []
        for _to in to_list:
            _users_list.append(To(_to))
        message.to = _users_list

        if image:
            ext = str(content_type).split("/")[1]
            timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
            message.attachment = Attachment(
                FileContent(image),
                FileName(f'event_image-{timestamp}.{ext}'),
                FileType(str(content_type)),
                Disposition('attachment'))

        if send_at:
            message.send_at = SendAt(self.get_unix_time(send_at), p=0)

        message.content = Content(MimeType.html, html_content)
        return message

    def send_email(self, email_to_send: Mail) -> None:
        """
        Send the email.

        Params:
        ------
        email_to_send: Mail - The sendgrid email object to send.
        """

        self.sendgrid.send(email_to_send)

    def get_unix_time(self, date_time: datetime) -> int:
        """
        Convert a datetime object into unix timestamp.
        """
        return int(time.mktime(date_time.timetuple()))
