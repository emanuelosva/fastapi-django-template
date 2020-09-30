"""
User model.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


#######################################
#             User DB Model           #
#######################################


class User(AbstractUser):
    """
    Custom user model.
    """

    # Unwanted properties
    username = None
    first_name = None
    last_name = None

    # Email as user unique identifier
    email = models.EmailField(
        _("Email address"),
        unique=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # Extra properties
    name = models.TextField(verbose_name="Name", max_length=124)
    password = models.TextField(max_length=1240)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
