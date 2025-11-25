from rest_framework_simplejwt.views import TokenObtainPairView
from authentication.serializers.auth import TokenObtainPairSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class LoginAPI(TokenObtainPairView):
  serializer_class = TokenObtainPairSerializer
  def post(self, request, *args, **kwargs):
    response = super().post(request, *args, **kwargs)
    if response.status_code != 200:
      return Response({"status": False, "error": "Invalid credentials"}, status=response.status_code)
    tokens = response.data
    custom_response = {
      "status": True,
      "message": "User logged in successfully",
      "tokens": {"access": tokens.get("access"), "refresh": tokens.get("refresh")}
    }
    return Response(custom_response, status=response.status_code)

class RegistrationAPI(APIView):
  permission_classes = [AllowAny]
  def post(self, request, *args, **kwargs):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
      user = serializer.save()
      return Response({"status": True, "message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    return Response({"status": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


