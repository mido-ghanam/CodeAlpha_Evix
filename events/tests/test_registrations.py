from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from ..models import Event, EventRegistration
from django.utils import timezone
from datetime import timedelta


class RegistrationFlowTests(TestCase):
  def setUp(self):
    self.client = APIClient()
    self.user = User.objects.create_user(username='user1', password='pass')
    self.staff = User.objects.create_user(username='staff', password='pass', is_staff=True)
    self.event = Event.objects.create(
      title='Test', start_date=timezone.now() + timedelta(days=1), end_date=timezone.now() + timedelta(days=2), capacity=2
    )

  def test_register_and_unregister(self):
    self.client.force_authenticate(user=self.user)
    url = f'/api/events/{self.event.id}/register/'
    # register
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 201)
    self.assertTrue(EventRegistration.objects.filter(user=self.user, event=self.event).exists())

    # double register -> 200 with already registered
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 200)

    # unregister
    resp = self.client.delete(url)
    self.assertEqual(resp.status_code, 200)
    self.assertFalse(EventRegistration.objects.filter(user=self.user, event=self.event).exists())

  def test_check_in_self(self):
    # register first
    EventRegistration.objects.create(user=self.user, event=self.event)
    self.client.force_authenticate(user=self.user)
    url = f'/api/events/{self.event.id}/check-in/'
    resp = self.client.post(url)
    self.assertEqual(resp.status_code, 200)
    reg = EventRegistration.objects.get(user=self.user, event=self.event)
    self.assertTrue(reg.checked_in)

  def test_check_in_other_requires_staff(self):
    other = User.objects.create_user(username='other', password='pass')
    EventRegistration.objects.create(user=other, event=self.event)
    # non-staff cannot check in others
    self.client.force_authenticate(user=self.user)
    url = f'/api/events/{self.event.id}/check-in/'
    resp = self.client.post(url, {'user_id': other.id})
    self.assertEqual(resp.status_code, 403)
    # staff can
    self.client.force_authenticate(user=self.staff)
    resp = self.client.post(url, {'user_id': other.id})
    self.assertEqual(resp.status_code, 200)
