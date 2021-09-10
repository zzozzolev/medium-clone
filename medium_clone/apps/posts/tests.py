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

        data["username"] = "test2"
        data["email"] = "test2@test.com"
        client.post(reverse("register"), data, format="json")

        cls.user1 = User.objects.get(username="test1")
        cls.user2 = User.objects.get(username="test2")

        client.force_authenticate(user=cls.user1)

        data = {
            "title": "test",
            "body": "test"
        }
        response = client.post(reverse("post-list"), data, format="json")
        cls.user1_slug1 = response.data["slug"]

        data = {
            "title": "test2",
            "body": "test2"
        }
        response = client.post(reverse("post-list"), data, format="json")
        cls.user1_slug2 = response.data["slug"]

    def test_no_account_user_create_post(self):
        """
        User which doesn't have a account can't create a post.
        """
        self.client.force_authenticate(user=None)
        res = self.client.post(reverse("post-list"))
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_allowany(self):
        """
        Anyone can retireve other post even anonymous user.
        """
        # Unset credentials
        self.client.force_authenticate(user=None)
        res = self.client.get(
            reverse("post-detail", kwargs={"slug": self.user1_slug1}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_list_allowany(self):
        """
        Anyone can list other post even anonymous user.
        """
        # Unset credentials
        self.client.force_authenticate(user=None)
        res = self.client.get(reverse("post-list"), {"author": "test1"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_non_existent_author_404(self):
        """
        Raise 404 for a non-existent author.
        """
        self.client.force_authenticate(user=None)
        res = self.client.get(reverse("post-list"), {"author": "fsweru"})
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_no_author_query_param(self):
        """
        Raise 400 if author query param is not given.
        """
        res = self.client.get(reverse("post-list"))
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_update_post(self):
        """
        Update the post.
        """
        # body is also required.
        data = {
            "title": "temp"
        }
        self.client.force_authenticate(user=self.user1)
        res = self.client.patch(
            reverse("post-detail", kwargs={"slug": self.user1_slug1}), data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_post_author_only(self):
        """
        Allow author only to update his/her post.
        """
        data = {
            "title": "temp"
        }
        self.client.force_authenticate(user=self.user2)
        res = self.client.patch(
            reverse("post-detail", kwargs={"slug": self.user1_slug2}), data)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_destroy_post_author_only(self):
        """
        Allow author only to destroy his/her post.
        """
        self.client.force_authenticate(user=self.user2)
        res = self.client.delete(
            reverse("post-detail", kwargs={"slug": self.user1_slug2}))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
