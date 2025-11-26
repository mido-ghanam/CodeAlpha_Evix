from django.urls import path, include
from django.contrib import admin

urlpatterns = [
  path('admin/', admin.site.urls),
  path("auth/", include("authentication.urls.web")),
  path("events/", include("events.urls.web")),
  
  ## APIs section ##
  path("api/auth/", include("authentication.urls.api")),
  path("api/events/", include("events.urls.api")),
]
