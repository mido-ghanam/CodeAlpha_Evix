from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as BaseTokenSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from core.utils import getUserTokens

class RegisterSerializer(serializers.ModelSerializer):
  first_name = serializers.CharField()
  last_name = serializers.CharField()
  username = serializers.CharField()
  password = serializers.CharField(write_only=True)
  email = serializers.EmailField()
  class Meta:
    model = User
    fields = [
      "first_name", "last_name", "username", "email", "password",
    ]

  def validate_username(self, value):
    if User.objects.filter(username=value).exists():
      raise serializers.ValidationError("username exists")
    return value

  def validate_email(self, value):
    if User.objects.filter(email=value).exists():
      raise serializers.ValidationError("email address exists")
    return value

  def create(self, validated_data):
    user = User.objects.create_user(
      first_name=validated_data.get('first_name', ''),
      last_name=validated_data.get('last_name', ''),
      username=validated_data['username'],
      email=validated_data['email'],
      password=validated_data['password'],
    )
    return {
      "status": True,
      "tokens": getUserTokens(user),
    }
  
class TokenObtainPairSerializer(BaseTokenSerializer):
  @classmethod
  def get_token(cls, user):
    token = super().get_token(user)
    token["full_name"] = user.get_full_name()
    token['username'] = user.username
    token['email'] = user.email
    token['is_staff'] = user.is_staff
    token['role'] = 'admin' if user.is_staff else 'user'
    return token
