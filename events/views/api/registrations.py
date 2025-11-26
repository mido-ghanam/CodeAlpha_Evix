from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone

from ...models import Event, EventRegistration
from ...serializers import EventSerializer, EventRegistrationSerializer
from django.contrib.auth import get_user_model


class IsAdminOrOwner(permissions.BasePermission):
  def has_permission(self, request, view):
    return bool(request.user and request.user.is_authenticated)

  def has_object_permission(self, request, view, obj):
    return request.user.is_staff or obj.user == request.user


class RegisterAPI(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def post(self, request, pk):
    with transaction.atomic():
      event = get_object_or_404(Event.objects.select_for_update(), pk=pk)
      user = request.user
      # check if already registered
      if EventRegistration.objects.filter(user=user, event=event).exists():
        return Response({"status": False, "message": "already registered"}, status=status.HTTP_200_OK)

      # check capacity if set
      if event.capacity is not None:
        # if seats_left is maintained, ensure >0; if not set, infer
        if getattr(event, 'seats_left', None) is not None:
          if event.seats_left is None or event.seats_left <= 0:
            return Response({"status": False, "message": "event is full"}, status=status.HTTP_400_BAD_REQUEST)
          event.seats_left -= 1
          event.save()

      EventRegistration.objects.create(user=user, event=event)
      return Response({"status": True, "message": "registered"}, status=status.HTTP_201_CREATED)

  def delete(self, request, pk):
    with transaction.atomic():
      event = get_object_or_404(Event.objects.select_for_update(), pk=pk)
      user = request.user
      deleted, _ = EventRegistration.objects.filter(user=user, event=event).delete()
      if deleted:
        # restore seat if applicable
        if getattr(event, 'seats_left', None) is not None:
          event.seats_left = (event.seats_left or 0) + 1
          event.save()
        return Response({"status": True, "message": "unregistered"}, status=status.HTTP_200_OK)
    return Response({"status": False, "message": "not registered"}, status=status.HTTP_404_NOT_FOUND)


class UserRegistrationsAPI(generics.ListAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = EventSerializer

  def get_queryset(self):
    user = self.request.user
    return Event.objects.filter(registrations__user=user).order_by('-start_date')


class EventRegistrationsAPI(generics.ListAPIView):
  permission_classes = [permissions.IsAdminUser]

  def list(self, request, pk=None):
    event = get_object_or_404(Event, pk=pk)
    regs = event.registrations.select_related('user')
    users = [reg.user for reg in regs]
    # serialize minimal user info
    data = [{"id": u.id, "username": getattr(u, 'username', None), "email": getattr(u, 'email', None)} for u in users]
    return Response({"status": True, "count": len(data), "users": data})

class CheckInAPI(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def post(self, request, pk):
    event = get_object_or_404(Event, pk=pk)
    user_id = request.data.get('user_id')
    if user_id:
      # only staff can check-in others
      if not request.user.is_staff:
        return Response({"status": False, "message": "forbidden"}, status=status.HTTP_403_FORBIDDEN)
      User = get_user_model()
      user = get_object_or_404(User, pk=user_id)
    else:
      user = request.user

    reg = EventRegistration.objects.filter(user=user, event=event).first()
    if not reg:
      return Response({"status": False, "message": "not registered"}, status=status.HTTP_404_NOT_FOUND)
    if reg.checked_in:
      return Response({"status": False, "message": "already checked-in"}, status=status.HTTP_200_OK)
    reg.checked_in = True
    reg.check_in_at = timezone.now()
    reg.save()
    return Response({"status": True, "message": "checked-in"})


class CheckInListAPI(generics.ListAPIView):
  permission_classes = [permissions.IsAuthenticated]

  def list(self, request, pk=None):
    event = get_object_or_404(Event, pk=pk)
    regs = event.registrations.filter(checked_in=True).select_related('user')
    data = [{"user_id": r.user.id, "username": getattr(r.user, 'username', None), "check_in_at": r.check_in_at} for r in regs]
    return Response({"status": True, "count": len(data), "checked_in": data})
