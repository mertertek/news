from rest_framework import serializers
from .models import CustomUser, Editor
from datetime import date
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

class UserRegisterationSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("id","name","email","password")

    def create(self, validated_date):
        return CustomUser.objects.create_user(**validated_date)

class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("id","email","password")

    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")

class EditorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editor
        fields = "__all__"