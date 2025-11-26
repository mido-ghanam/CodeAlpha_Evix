from django.urls import path, include
from django.contrib import admin
from events.views.api import registrations as events_registrations

urlpatterns = [
  path('admin/', admin.site.urls),
  path("auth/", include("authentication.urls.web")),
  path("events/", include("events.urls.web")),
  
  ## APIs section ##
  path("api/auth/", include("authentication.urls.api")),
  path("api/events/", include("events.urls.api")),
  path("api/users/me/registrations/", events_registrations.UserRegistrationsAPI.as_view()),
]
