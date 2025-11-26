from django.contrib import admin
from .models import Event
from .models import EventRegistration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

  list_display = ('title', 'start_date', 'end_date', 'is_active', 'organizer')
  list_filter = ('is_active', 'category')
  search_fields = ('title', 'description')


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
  list_display = ('user', 'event', 'checked_in', 'created_at')
  list_filter = ('checked_in',)
  search_fields = ('user__username', 'event__title')

