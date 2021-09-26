from django.utils.text import slugify
from rest_framework import serializers

from apps.common.utils import generate_random_string
from apps.profiles.serializers import ProfileSerializer

from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = ProfileSerializer(read_only=True)
    liked = serializers.SerializerMethodField()
    # TODO: liked_num
    is_update_key = "is_update"
    SLUG_MAX_LENGTH = Post._meta.get_field("slug").max_length
    BODY_MAX_LENGTH = Post._meta.get_field("body").max_length
    UNIQUE_SIZE = 12

    class Meta:
        model = Post
        fields = ("author", "title", "slug", "body",
                  "description", "created_at", "updated_at", "liked")
        extra_kwargs = {
            "title": {"required": True},
            # slug is made of title.
            "slug": {"read_only": True},
            "body": {"required": True},
            # description is given or made of body.
            "description": {"required": False},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True}
        }

    def create(self, validated_data):
        author = self.context["author"]
        post = Post.objects.create(author=author, **validated_data)

        return post

    def to_internal_value(self, data):
        # Set default values only by create method call.
        if not self.context[self.is_update_key]:
            self.set_slug_by_title(data)
            self.set_description_by_body(data)

        return data

    def get_liked(self, instance):
        user = self.context.get("user", None)

        if user is None:
            return False

        # Handle Anonymous user like display.
        if not user.is_authenticated:
            return False

        return user.profile.has_liked(instance)

    def set_slug_by_title(self, data):
        slug = slugify(data["title"])
        # default size is 12
        unique = generate_random_string(self.UNIQUE_SIZE)

        unique_hypen_length = len(unique) + 1
        if len(slug) + unique_hypen_length > self.SLUG_MAX_LENGTH:
            slug = slug[:self.SLUG_MAX_LENGTH - unique_hypen_length]
            if slug[-1] == "-":
                slug = slug[:-1]

        data["slug"] = slug + "-" + unique

    def set_description_by_body(self, data):
        if "description" not in data:
            data["description"] = data["body"][:self.BODY_MAX_LENGTH]
