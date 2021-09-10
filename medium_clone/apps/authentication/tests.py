from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        client = cls.client_class()
        cls.data = {
            "username": "test",
            "password": "test4321",
            "password2": "test4321",
            "email": "test@test.com",
            "first_name": "test",
            "last_name": "test"
        }
        client.post(reverse("register"), cls.data, format="json")

    def setUp(self):
        # Make Email different for every method.
        self.data["Email"] = f"{self._testMethodName}@test.com"

    def test_not_same_email(self):
        """
        Users never have same email.
        """
        self.data["username"] = self._testMethodName
        res = self.client.post(reverse("register"), self.data, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_hashed(self):
        """
        User's password must be hashed.
        """
        res = self.client.post(reverse("register"), self.data, format="json")
        # TODO: user 정보 얻어오는 api가 개발되면 password 가져와서 비교하기

    def test_jwt(self):
        """
        Test whether jwt works well or not.
        """
        res = self.client.post(reverse("token_obtain_pair"), data={
            "username": self.data["username"], "password": self.data["password"]}, format="json")
        res = self.client.post(reverse("token_refresh"), data={
                               "refresh": res.json()["refresh"]}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)
