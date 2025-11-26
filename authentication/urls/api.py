from ..views import api as apiV
from django.urls import path

urlpatterns = [
  path("login/", apiV.auth.LoginAPI.as_view(), name="LoginAPI"),
  path("registration/", apiV.auth.RegistrationAPI.as_view(), name="RegistrationAPI"),
  path("logout/", apiV.auth.LogoutAPI.as_view(), name="LogoutAPI"),
  path("me/", apiV.auth.MeAPI.as_view(), name="LogoutAPI"),

]
