"""
WSGI config for {app} project.
"""

import os

from django.core.wsgi import get_wsgi_application
from fastapi import FastAPI


#######################################
#       Django WSGI Application       #
#######################################

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
application = get_wsgi_application()


#######################################
#         FastAPI Application         #
#######################################

# The django wsgi application must be initialize first.
# This schema allows to the fastAPI application can access to
# the django environ and application process.
# The principal usage of this schema is access to DjangoORM
# in the fastAPI process.

from app.urls import api_router

app = FastAPI(
    title="{{ app }}",
    description="A fastAPI-Django integration template",
    version="1.0.0",
)

app.include_router(api_router, prefix="/api")
