from rest_framework.test import APITestCase

from .models import Post
from .serializers import PostSerializer


class PostSerializerTests(APITestCase):
    def test_slug_equal_length(self):
        data = {
            "title": "a" *
            (PostSerializer.SLUG_MAX_LENGTH - PostSerializer.UNIQUE_SIZE)
        }
        serializer = PostSerializer()
        serializer.set_slug_by_title(data)

        self.assertEqual(len(data["slug"]), PostSerializer.SLUG_MAX_LENGTH)

    def test_slug_gt_length(self):
        data = {"title": "a" * PostSerializer.SLUG_MAX_LENGTH}
        serializer = PostSerializer()
        serializer.set_slug_by_title(data)

        self.assertEqual(len(data["slug"]), PostSerializer.SLUG_MAX_LENGTH)

    def test_slug_last_hypen(self):
        data = {
            "title": "a" *
            (PostSerializer.SLUG_MAX_LENGTH - PostSerializer.UNIQUE_SIZE - 1)
        }
        data["title"] += "-"
        serializer = PostSerializer()
        serializer.set_slug_by_title(data)

        self.assertNotRegex(data["slug"], "--")
