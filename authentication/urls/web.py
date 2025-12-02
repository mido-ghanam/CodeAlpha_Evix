from django.urls import path
from authentication.views import web as webV

urlpatterns = [
  path("login/", webV.auth.login, name="login"),
  path("signup/", webV.auth.registration, name="register"),

]
