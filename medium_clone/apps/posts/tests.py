from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
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

    def test_not_empty_description(self):
        """
        Test whether description is empty or not when description is not given.
        """
        data = {
            "body": "test"
        }
        self.serializer.set_description_by_body(data)

        self.assertTrue("description" in data)


class PostViewSetTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        client = cls.client_class()

        data = {
            "username": "test1",
            "password": "test4321",
            "password2": "test4321",
            "email": "test@test.com",
            "first_name": "test",
            "last_name": "test"
        }

        client.post(reverse("register"), data, format="json")
        client.post(reverse("get-auth-token"),
                    {"username": "test1", "password": "test4321"})
        user1_token = User.objects.get(username="test1").auth_token

        data = {
            "title": "test",
            "body": "test"
        }

        client.credentials(HTTP_AUTHORIZATION=f"Token {user1_token}")
        response = client.post(reverse("post-list"), data, format="json")
        cls.user1_slug = response.data["slug"]

    def test_retrieve_allowany(self):
        """
        Anyone can retireve other post even anonymous user.
        """
        # Unset credentials
        self.client.credentials()
        res = self.client.get(
            reverse("post-detail", kwargs={"slug": self.user1_slug}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_allowany(self):
        """
        Anyone can list other post even anonymous user.
        """
        # Unset credentials
        self.client.credentials()
        res = self.client.get(reverse("post-list"), {"author": "test1"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_non_existent_author_404(self):
        """
        Raise 404 for a non-existent author.
        """
        self.client.credentials()
        res = self.client.get(reverse("post-list"), {"author": "fsweru"})
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
