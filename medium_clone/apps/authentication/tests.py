from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RegistrationTests(APITestCase):
    def test_not_same_email(self):
        """
        Users never have same email.
        """
        data = {"username": "test", "password": "test1234",
                "password2": "test1234", "Email": "test@test.com", "first_name": "test", "last_name": "test"}
        url = reverse("register")
        _ = self.client.post(url, data, format="json")
        res = self.client.post(url, data, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
