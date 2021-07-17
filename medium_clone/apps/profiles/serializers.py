from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = Profile
        fields = ("bio", "username", "email")
        extra_kwargs = {
            "bio": {"required": False}
        }
