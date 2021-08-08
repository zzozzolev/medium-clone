from rest_framework.test import APITestCase

from .models import Post
from .serializers import PostSerializer


class PostSerializerTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.serializer = PostSerializer()

    def test_slug_equal_length(self):
        """
        Test slug which has maximum length except for unique size.
        """
        data = {
            "title": "a" *
            (PostSerializer.SLUG_MAX_LENGTH - PostSerializer.UNIQUE_SIZE)
        }
        self.serializer.set_slug_by_title(data)

        self.assertEqual(len(data["slug"]), PostSerializer.SLUG_MAX_LENGTH)

    def test_slug_gt_length(self):
        """
        Test slug which has maximum length.
        """
        data = {"title": "a" * PostSerializer.SLUG_MAX_LENGTH}
        self.serializer.set_slug_by_title(data)

        self.assertEqual(len(data["slug"]), PostSerializer.SLUG_MAX_LENGTH)

    def test_slug_last_hypen(self):
        """
        Test slug which has hypen at last part.
        """
        data = {
            "title": "a" *
            (PostSerializer.SLUG_MAX_LENGTH - PostSerializer.UNIQUE_SIZE - 1)
        }
        data["title"] += "-"
        self.serializer.set_slug_by_title(data)

        self.assertNotRegex(data["slug"], "--")