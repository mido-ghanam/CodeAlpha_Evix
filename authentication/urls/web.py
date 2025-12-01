from django.urls import path
from authentication.views import web as webV

urlpatterns = [
  path("login/", webV.login, name="login"),
  path("signup/", webV.registration, name="register"),

]
