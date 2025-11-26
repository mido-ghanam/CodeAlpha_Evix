from django.urls import path 
from . import views as v

urlpatterns = [
  path("", v.index, name="index"),
  path("auth/login/", v.login, name="login"),
]
