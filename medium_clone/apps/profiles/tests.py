from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Profile


class ProfileRetrieveUpdateTests(APITestCase):
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

        client.post(reverse("get-auth-token"),
                    {"username": "test1", "password": "test4321"})
        cls.user1_token = User.objects.get(username="test1").auth_token

    def test_retrieve_allowany(self):
        """
        Anyone can retireve other profile.
        """
        res = self.client.get(
            reverse("profile_retrieveupdate_view", kwargs={"username": "test1"}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_update_profile_owner_only(self):
        """
        Allow owner only to update his/her profile.
        """
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user1_token}")
        res = self.client.patch(
            reverse("profile_retrieveupdate_view", kwargs={"username": "test2"}))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_modify_partial(self):
        """
        Client can modify a part of the profile.
        """
        data = {"bio": "awesome", "username": "test1",
                "email": "email@test.com"}
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.user1_token}")
        res = self.client.patch(
            reverse("profile_retrieveupdate_view", kwargs={"username": "test1"}), data, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_put_not_allowed(self):
        """
        Client can't use put method.
        """
        data = {"bio": "awesome", "username": "test1",
        "email": "email@test.com"}
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.user1_token}")
        res = self.client.put(
            reverse("profile_retrieveupdate_view", kwargs={"username": "test1"}), data, format="json")
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)       
 