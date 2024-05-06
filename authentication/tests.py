from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class SignInSerializerTestCase(APITestCase):
    def setUp(self):
        # this user already set in seeding migrate
        self.username = "admin"
        self.password = "admin!@#"

    def test_valid_login(self):
        url = reverse("authentication:signin")
        data = {"username": self.username, "password": self.password}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertIn("name", response.data)
        self.assertIn("id", response.data)
        self.assertIn("username", response.data)

    def test_invalid_login(self):
        url = reverse("authentication:signin")
        data = {"username": self.username, "password": "wrongpassword"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertNotIn("token", response.data)
        self.assertNotIn("name", response.data)
        self.assertNotIn("id", response.data)
        self.assertNotIn("username", response.data)
