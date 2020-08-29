"""
Error Logger Module
"""

import traceback
from datetime import datetime

from db.db import get_collection, CRUD
from mails.sender import EmailSender

from config import settings  # pylint: disable-msg=E0611


###########################################
##          Error Logger Class           ##
###########################################


class ErroLogger:
    """
    Error logger implementation
    """

    def __init__(self):
        self.sender = EmailSender()
        self.collection = get_collection("error")
        self.crud = CRUD(self.collection)

    async def register(self, _exception):
        """
        Create a complete report for exception.
        """
        error_dict = self.format_db(_exception)

        # Notify the admin
        self.send_email_to_admin(error_dict)
        # Save on db
        await self.crud.create(error_dict)

    def format_db(self, _exception):
        """
        Add the error on db
        """
        date = datetime.now()
        filename = __name__
        error_to_str = self.exception_to_string(_exception)
        error = {
            "date": date,
            "filename": filename,
            "exception": error_to_str
        }
        return error

    def send_email_to_admin(self, dict_error: dict) -> None:
        """
        Send a email to admin of the error.
        """
        message = self.generate_message(dict_error)
        to_list = [settings.EMAIL_ADMIN]

        email = self.sender.create_email(
            to_list=to_list,
            subject="UNU API ERROR",
            html_content=message)

        self.sender.send.send_email(email)

    def exception_to_string(self, excp):
        """
        Transform a exception to string.
        """
        stack = traceback.extract_stack(
        )[:-3] + traceback.extract_tb(excp.__traceback__)
        pretty = traceback.format_list(stack)
        return ''.join(pretty) + '\n  {} {}'.format(excp.__class__, excp)

    def generate_message(self, dict_error: dict) -> str:
        """
        Generates a message from error dict.
        """
        return f"""
        <h2>A error was occur in UNU-API.</h2>
        <ul>
          <li><h4>File: {dict_error["filename"]}</h4></li>
          <li><h4>Date: {dict_error["date"]}</h4></li>
          <li><h4>Error: {dict_error["exception"]}</h4></li>
        </ul>
        """


error_logger = ErroLogger()
