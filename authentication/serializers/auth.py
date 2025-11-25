from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as BaseTokenSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from core.utils import getUserTokens
from .. import models as m


class RegisterSerializer(serializers.ModelSerializer):
  username = serializers.CharField()
  password = serializers.CharField(write_only=True)
  email = serializers.EmailField()
  medications = serializers.CharField(required=False, allow_blank=True, allow_null=True)
  age = serializers.IntegerField(required=False, allow_null=True)
  height = serializers.FloatField(required=False, allow_null=True)
  weight = serializers.FloatField(required=False, allow_null=True)
  allergies = serializers.CharField(required=False, allow_blank=True, allow_null=True)
  gender = serializers.CharField(required=False, allow_blank=True, allow_null=True)
  diseases = serializers.CharField(required=False, allow_blank=True, allow_null=True)

  class Meta:
    model = User
    fields = [
      "first_name", "last_name", "username", "email", "password",
      "medications", "age", "weight", "height",
      "allergies", "gender", "diseases"
    ]

  def validate_username(self, value):
    if User.objects.filter(username=value).exists():
      raise serializers.ValidationError("اسم المستخدم مستخدم بالفعل.")
    return value

  def validate_email(self, value):
    if User.objects.filter(email=value).exists():
      raise serializers.ValidationError("البريد الإلكتروني مستخدم بالفعل.")
    return value

  def create(self, validated_data):
    user = User.objects.create_user(
      first_name=validated_data.get('first_name', ''),
      last_name=validated_data.get('last_name', ''),
      username=validated_data['username'],
      email=validated_data['email'],
      password=validated_data['password'],
    )

    user_profile = m.Users.objects.create(
      user=user,
      medications=validated_data.get('medications') or '',
      weight=validated_data.get("weight"),
      height=validated_data.get("height"),
      age=validated_data.get('age'),
      allergies=validated_data.get('allergies') or '',
      gender=validated_data.get('gender') or '',
      diseases=validated_data.get('diseases') or '',
    )

    return {
      "status": True,
      "tokens": getUserTokens(user),
      "weight": user_profile.weight,
      "height": user_profile.height,
      "age": user_profile.age,
      "medications": user_profile.medications,
      "allergies": user_profile.allergies,
      "gender": user_profile.gender,
      "diseases": user_profile.diseases,
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
