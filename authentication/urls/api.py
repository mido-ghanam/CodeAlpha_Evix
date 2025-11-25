from ..views import api as apiV
from django.urls import path

urlpatterns = [
  path("login/", apiV.auth.LoginAPI.as_view(), name="LoginAPI"),
]
