from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        email = "test@example.com"
        password = "testpass123"
        user = User.objects.create_user(
            username="testuser", email=email, password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_new_user_email_normalized(self):
        user = User.objects.create_user(
            username="testuser2", email="test@EXAMPLE.COM", password="pass123"
        )
        self.assertEqual(user.email, "test@example.com")


class UserAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = "/users/register/"

    def test_user_registration_success(self):
        payload = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "securepass456",
        }
        response = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_registration_with_existing_email_fails(self):
        User.objects.create_user(
            username="duplicate", email="duplicate@example.com", password="pass123"
        )
        payload = {
            "username": "duplicate",
            "email": "duplicate@example.com",
            "password": "anotherpass789",
        }
        response = self.client.post(self.register_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
