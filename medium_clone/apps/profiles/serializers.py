from django.db import transaction
from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")
    email = serializers.EmailField(source="user.email")

    def update(self, instance, validated_data):
        user = instance.user
        user_data = validated_data.pop("user")

        for key, value in user_data.items():
            setattr(user, key, value)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        with transaction.atomic():
            instance.save()
            user.save()

        return instance

    class Meta:
        model = Profile
        fields = ("bio", "username", "email")
        extra_kwargs = {
            "bio": {"required": False}
        }
