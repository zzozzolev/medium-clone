from typing import Any, Mapping, Type

from django.db import transaction
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from apps.profiles.models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[
                                   UniqueValidator(queryset=User.objects.only("email"))])
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username", "password", "password2",
                  "email", "first_name", "last_name")
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True}
        }

    def validate(self, attrs: Mapping[str, Any]) -> Mapping[str, Any]:
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password2": "Type your password2 exactly as password"})

        return attrs

    @transaction.atomic
    def create(self, validated_data: Mapping[str, Any]) -> Type[User]:
        # create_user already makes password hashed using make_password
        # Just pass validate password to create_user
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"]
        )

        Profile.objects.create(user=user)

        return user
