# accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'full_name', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user:
            if not user.is_active:
                raise serializers.ValidationError("Please verify your email first.")
            return user
        raise serializers.ValidationError("Invalid credentials")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name', 'is_active', 'is_staff']
