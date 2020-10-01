"""
{{ project_name }} URL Configuration (Router integration)
"""

from django.contrib import admin
from django.urls import path

from fastapi import APIRouter
from users.urls import router as user_router

#######################################
#         Url for django App          #
#######################################

# Only django can access to the `urlpatterns`.
# By for default only the admin panel is needed,
# all other any route is manage by FastAPI.

urlpatterns = [
    path("admin/", admin.site.urls),
]


#######################################
#   Api Router (merge all routers)    #
#######################################

api_router = APIRouter()

# All router must be included here.

api_router.include_router(user_router, prefix="/users", tags=["Users"])
