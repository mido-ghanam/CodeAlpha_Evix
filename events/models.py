from django.db import models
import uuid
from django.conf import settings


class Event(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  title = models.CharField(max_length=200)
  description = models.TextField(blank=True)
  is_online = models.BooleanField(default=False)
  location = models.CharField(max_length=255, null=True, blank=True)
  location_url = models.URLField(null=True, blank=True)
  start_date = models.DateTimeField()
  end_date = models.DateTimeField(null=True, blank=True)
  capacity = models.PositiveIntegerField(null=True, blank=True)
  max_per_user = models.PositiveIntegerField(null=True, blank=True)
  seats_left = models.PositiveIntegerField(null=True, blank=True)
  auto_close = models.BooleanField(default=False)
  registration_deadline = models.DateTimeField(null=True, blank=True)
  is_active = models.BooleanField(default=True)
  category = models.CharField(max_length=100, blank=True)
  organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
  updated_at = models.DateTimeField(auto_now=True)
  created_at = models.DateTimeField(auto_now_add=True)
  banner = models.ImageField(upload_to='event_banners/', null=True, blank=True)

  def __str__(self):
    return self.title

  def save(self, *args, **kwargs):
    # initialize seats_left from capacity on first save if not set
    if self.capacity and (self.seats_left is None):
      try:
        # if this is a new instance (no pk yet) or seats_left is unset, set it
        self.seats_left = self.capacity
      except Exception:
        pass
    super().save(*args, **kwargs)


class EventRegistration(models.Model):
  id = models.BigAutoField(primary_key=True)
  user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
  event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
  created_at = models.DateTimeField(auto_now_add=True)
  checked_in = models.BooleanField(default=False)
  check_in_at = models.DateTimeField(null=True, blank=True)

  class Meta:
    unique_together = ('user', 'event')

  def __str__(self):
    return f"{self.user.username} -> {self.event.title}"

