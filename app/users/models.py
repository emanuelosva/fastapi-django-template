"""
User model.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):
    """
    Custom user model.
    """
    # Email as user unique identifier
    username = None
    email = models.EmailField(
        _("Email address"),
        unique=True,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    name = models.TextField(verbose_name="Name", max_length=124)

    password = models.TextField(max_length=1240)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)
