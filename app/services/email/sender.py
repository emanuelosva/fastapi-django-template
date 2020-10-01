"""
Email sender class.
"""

import time
from typing import List
from datetime import datetime

from sendgrid import SendGridAPIClient, SendGridException
from sendgrid.helpers import mail
from fastapi import HTTPException

from app.settings import SENDGRID_API_KEY, EMAIL_DOMAIM


#######################################
#            Mailing Class            #
#######################################


class EmailSender:
    """
    Email sender.
    """

    def __init__(self):
        self.sendgrid = SendGridAPIClient(api_key=SENDGRID_API_KEY)
        self.from_email = EMAIL_DOMAIM

    def create_email(
        self,
        to_list: List[str],
        subject: str,
        html_content: str,
        image: bytes = None,
        content_type: str = None,
        send_at: datetime = None,
    ) -> mail.Mail:
        """
        Create a new sendgrid email object.

        Params:
        - to_list: List[str] - The recipients list.
        - subject: str - The email subject.
        - html_content: str - HTML text to fill the email.
        - image: bytes - A optional image to attachment in email.
        - content_type: str - The content type of the image.
        - send_at: datetime - The datetime when the email must be sended.
        Return:
        - message: Mail - The sendgrid email object.
        """
        message = mail.Mail()
        message.from_email = mail.From(self.from_email)
        message.subject = mail.Subject(subject)

        _users_list = []
        for _to in to_list:
            _users_list.append(mail.To(_to))
        message.to = _users_list

        if image:
            ext = str(content_type).split("/")[1]
            timestamp = datetime.utcnow().strftime("%Y-%m-%d-%H%M%S")
            message.attachment = mail.Attachment(
                mail.FileContent(image),
                mail.FileName(f"event_image-{timestamp}.{ext}"),
                mail.FileType(str(content_type)),
                mail.Disposition("attachment"),
            )

        if send_at:
            message.send_at = mail.SendAt(self.get_unix_time(send_at), p=0)

        message.content = mail.Content(mail.MimeType.html, html_content)
        return message

    def send_email(self, email_to_send: mail.Mail) -> None:
        """
        Send the email.

        Params:
        email_to_send: Mail - The sendgrid email object to send.
        """
        try:
            self.sendgrid.send(email_to_send)
        except SendGridException:
            raise HTTPException(500, "Server Error")

    def get_unix_time(self, date_time: datetime) -> int:
        """
        Convert a datetime object into unix timestamp.
        """
        return int(time.mktime(date_time.timetuple()))
