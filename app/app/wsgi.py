"""
WSGI config for {app} project.
"""

import os

from django.core.wsgi import get_wsgi_application
from fastapi import FastAPI

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

application = get_wsgi_application()

app = FastAPI(
    title="Todo...",
    description="A fastAPI-Django integration template",
    version="1.0.0",
)
