from rest_framework import serializers

from apps.profiles.serializers import ProfileSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ("author", "title", "slug", "body", "description")
        extra_kwargs = {
            "title": {"required": True},
            # slug is made of title.
            "slug": {"read_only": True},
            "body": {"required": True},
            # description is given or made of body.
            "description": {"required": False}
        }
