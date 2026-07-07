from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.authentication.models.user import UserRole

User = get_user_model()


class UsersManagementTests(APITestCase):
    """
    Test suite for admin-facing customer management tools.
    """

    def setUp(self) -> None:
        self.admin = User.objects.create_user(
            email="admin@example.com",
            password="SecurePassword123!",
            role=UserRole.ADMIN,
        )
        self.support = User.objects.create_user(
            email="support@example.com",
            password="SecurePassword123!",
            role=UserRole.SUPPORT_AGENT,
        )
        self.customer = User.objects.create_user(
            email="customer@example.com",
            phone="03001234567",
            password="SecurePassword123!",
            full_name="John Doe",
            role=UserRole.CUSTOMER,
        )

        self.list_url = reverse("users:customer_list")
        self.block_url = reverse(
            "users:customer_block", kwargs={"pk": str(self.customer.id)}
        )

    def test_list_customers_support_agent(self) -> None:
        """
        Support agents are authorized to retrieve lists of customers.
        """
        self.client.force_authenticate(user=self.support)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["email"], "customer@example.com")

    def test_list_customers_customer_forbidden(self) -> None:
        """
        Regular customers are blocked from back-office lists.
        """
        self.client.force_authenticate(user=self.customer)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_search_customers(self) -> None:
        """
        Admins can search customers by name.
        """
        self.client.force_authenticate(user=self.admin)
        # Match search
        response = self.client.get(f"{self.list_url}?search=John")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 1)

        # No match search
        response = self.client.get(f"{self.list_url}?search=NotFound")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["data"]), 0)

    def test_block_customer_support_forbidden(self) -> None:
        """
        Support agents cannot block/unblock customers.
        """
        self.client.force_authenticate(user=self.support)
        payload = {"is_blocked": True}
        response = self.client.post(self.block_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_block_customer_admin_success(self) -> None:
        """
        Admins can block and unblock customer accounts.
        """
        self.client.force_authenticate(user=self.admin)

        # Block
        payload = {"is_blocked": True}
        response = self.client.post(self.block_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["data"]["is_blocked"])

        self.customer.refresh_from_db()
        self.assertTrue(self.customer.is_blocked)

        # Unblock
        payload = {"is_blocked": False}
        response = self.client.post(self.block_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["data"]["is_blocked"])

        self.customer.refresh_from_db()
        self.assertFalse(self.customer.is_blocked)

