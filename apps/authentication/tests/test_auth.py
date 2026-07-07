from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthenticationTests(APITestCase):
    """
    Unit tests for registration, login, profile, and token refresh endpoints.
    Verifies HTTP status codes and the standard API response structure.
    """

    def setUp(self) -> None:
        self.register_url = reverse("authentication:register")
        self.login_url = reverse("authentication:login")
        self.profile_url = reverse("authentication:profile")
        self.refresh_url = reverse("authentication:token_refresh")

        self.user_email = "testuser@example.com"
        self.user_password = "SecurePassword123!"
        self.user_data = {
            "email": self.user_email,
            "password": self.user_password,
            "password_confirm": self.user_password,
            "full_name": "Test User",
        }

        # Pre-create a user for login, profile, and refresh tests
        self.existing_user = User.objects.create_user(
            email="existing@example.com",
            password="SecurePassword123!",
            full_name="Existing User",
        )

    def test_register_user_success(self) -> None:
        """
        Verify successful user registration.
        """
        response = self.client.post(self.register_url, self.user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message"], "User registered successfully.")
        self.assertEqual(response.data["data"]["email"], self.user_email)
        self.assertEqual(response.data["data"]["full_name"], "Test User")

        self.assertNotIn("password", response.data["data"])
        self.assertIsNone(response.data["errors"])

    def test_register_user_password_mismatch(self) -> None:
        """
        Verify registration failure when passwords do not match.
        """
        data = self.user_data.copy()
        data["password_confirm"] = "DifferentPassword123!"
        response = self.client.post(self.register_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])
        self.assertEqual(response.data["message"], "Validation failed")
        self.assertIn("password_confirm", response.data["errors"])

    def test_register_user_duplicate_email(self) -> None:
        """
        Verify registration failure for a duplicate email address.
        """
        data = self.user_data.copy()
        data["email"] = "existing@example.com"
        response = self.client.post(self.register_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])
        self.assertIn("email", response.data["errors"])

    def test_login_user_success(self) -> None:
        """
        Verify successful login with valid credentials.
        """
        login_data = {
            "email": "existing@example.com",
            "password": "SecurePassword123!",
        }
        response = self.client.post(self.login_url, login_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["message"], "Login successful.")
        self.assertIn("access", response.data["data"]["tokens"])
        self.assertIn("refresh", response.data["data"]["tokens"])
        self.assertEqual(response.data["data"]["user"]["email"], "existing@example.com")

    def test_login_user_invalid_credentials(self) -> None:
        """
        Verify login failure with incorrect credentials.
        """
        login_data = {
            "email": "existing@example.com",
            "password": "WrongPassword123!",
        }
        response = self.client.post(self.login_url, login_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data["success"])
        self.assertEqual(response.data["message"], "Validation failed")
        self.assertIn("non_field_errors", response.data["errors"])

    def test_get_profile_authenticated(self) -> None:
        """
        Verify retrieving profile info for an authenticated user.
        """
        # Authenticate first by login
        login_data = {
            "email": "existing@example.com",
            "password": "SecurePassword123!",
        }
        login_response = self.client.post(self.login_url, login_data, format="json")
        access_token = login_response.data["data"]["tokens"]["access"]

        # Request profile with token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(response.data["data"]["email"], "existing@example.com")

    def test_get_profile_unauthenticated(self) -> None:
        """
        Verify retrieving profile fails when unauthenticated.
        """
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data["success"])
        self.assertEqual(response.data["message"], "Authentication credentials were not provided.")

    def test_token_refresh_success(self) -> None:
        """
        Verify refreshing an access token using a valid refresh token.
        """
        # Authenticate first by login
        login_data = {
            "email": "existing@example.com",
            "password": "SecurePassword123!",
        }
        login_response = self.client.post(self.login_url, login_data, format="json")
        refresh_token = login_response.data["data"]["tokens"]["refresh"]

        # Refresh
        refresh_data = {"refresh": refresh_token}
        response = self.client.post(self.refresh_url, refresh_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertIn("access", response.data["data"])

    def test_token_refresh_invalid(self) -> None:
        """
        Verify token refresh failure with an invalid refresh token.
        """
        refresh_data = {"refresh": "invalid-refresh-token"}
        response = self.client.post(self.refresh_url, refresh_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(response.data["success"])
