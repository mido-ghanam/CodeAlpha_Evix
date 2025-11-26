from rest_framework import serializers
from .models import Event, EventRegistration


class EventSerializer(serializers.ModelSerializer):
  class Meta:
    model = Event
    fields = [
      'id', 'title', 'description', 'is_online', 'location', 'location_url',
      'start_date', 'end_date', 'capacity', 'max_per_user', 'seats_left',
      'auto_close', 'registration_deadline', 'is_active', 'category', 'organizer',
      'created_at', 'updated_at',
    ]
    read_only_fields = ['id', 'created_at', 'updated_at', 'organizer']


class RegistrationSerializer(serializers.Serializer):
  event_id = serializers.UUIDField(required=True)


class EventRegistrationSerializer(serializers.ModelSerializer):
  user_username = serializers.CharField(source='user.username', read_only=True)

  class Meta:
    model = EventRegistration
    fields = ['user', 'user_username', 'event', 'created_at', 'checked_in', 'check_in_at']
    read_only_fields = ['created_at', 'checked_in', 'check_in_at']
