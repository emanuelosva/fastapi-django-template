"""
Email helpers.
"""

import base64
from typing import List
from datetime import datetime

from app.settings import SERVER_HOST
from .sender import EmailSender


###########################################
##       Email Sender Abstraction        ##
###########################################

sender = EmailSender()


#######################################
#           Mailing helpers           #
#######################################


def send_welcome_email(username: str, email: str) -> None:
    """
    Send a welcome email.

    Params:
    ------
    - username: str - The username of the new user
    - email: str - The target email
    """

    # TODO ...
    # Load html templates and get the content from it.
    # html_content = ...

    content = f"<h1>Welcome to app, {username}</h1>"
    email = sender.create_email(
        to_list=[email],
        subject=f"Welcome from {{ app }}",
        html_content=content,
    )
    sender.send_email(email_to_send=email)


def send_recovery_password_email(token: str, email: str) -> None:
    """
    Send a recovery password email.

    Params:
    ------
    - token: str - The encoded special token
    - email: str - The user email
    """

    # TODO ...
    # Load html templates and get the content from it.
    # html_content = ...

    # You must have to send this as a anchor
    # to my-domain.com/reset-password?token=ad5a....
    link = f"{SERVER_HOST}/reset-password?token={token}"
    content = f"""
    <h1>Reset your password</h1>
    <p></p>
    <a href="{link}" target="_blank" rel="noopener noreferrer">Press here</a>
    """
    email = sender.create_email(
        to_list=[email],
        subject=f"Recovery Password",
        html_content=content,
    )
    sender.send_email(email_to_send=email)
