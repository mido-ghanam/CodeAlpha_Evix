from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.utils import timezone

def default_expiry(ex=30): return timezone.now() + timedelta(minutes=ex)

def getUserTokens(user):
  refresh = RefreshToken.for_user(user)
  return {"refresh": str(refresh), "access": str(refresh.access_token),}
