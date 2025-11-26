from rest_framework_simplejwt.views import TokenObtainPairView
from authentication.serializers.auth import TokenObtainPairSerializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

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
    serializer = RegisterSerializer(data=request.data)
    if not serializer.is_valid():
      return Response({"status": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    return Response({"status": True, "message": "User registered successfully"}, status=status.HTTP_201_CREATED)
    
class LogoutAPI(APIView):
  permission_classes = [AllowAny]
  def post(self, request, *args, **kwargs):
    try:
      RefreshToken(request.data["refresh"]).blacklist()
      return Response({"status": True, "message": "User logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e: return Response({"status": False, "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MeAPI(APIView):
  permission_classes = [IsAuthenticated]
  def get(self, request, *args, **kwargs):
    user = request.user
    user_data = {
      "username": user.username,
      "email": user.email,
      "first_name": user.first_name,
      "last_name": user.last_name,
    }
    return Response({"status": True, "user": user_data}, status=status.HTTP_200_OK)
