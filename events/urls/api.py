from ..views import api as apiV
from django.urls import path

urlpatterns = [
  path("", apiV.events.EventsListCreateAPI.as_view(), name="EventsListAPI"),
  path("<uuid:pk>/", apiV.events.EventsDetailAPI.as_view(), name="EventDetailAPI"),
  path("<uuid:pk>/register/", apiV.registrations.RegisterAPI.as_view(), name="EventRegisterAPI"),
  path("<uuid:pk>/registrations/", apiV.registrations.EventRegistrationsAPI.as_view(), name="EventRegistrationsListAPI"),
  path("<uuid:pk>/check-in/", apiV.registrations.CheckInAPI.as_view(), name="EventCheckInAPI"),
  path("<uuid:pk>/check-in-list/", apiV.registrations.CheckInListAPI.as_view(), name="EventCheckInListAPI"),
  path("<uuid:pk>/upload-banner/", apiV.events.UploadBannerAPI.as_view(), name="EventUploadBannerAPI"),
  path("categories/", apiV.events.CategoriesAPI.as_view(), name="EventCategoriesAPI"),
]
