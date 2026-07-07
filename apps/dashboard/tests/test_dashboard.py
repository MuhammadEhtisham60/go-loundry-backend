from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.authentication.models.user import UserRole

User = get_user_model()


class DashboardTests(APITestCase):
    """
    Test suite for admin operations dashboard stats.
    """

    def setUp(self) -> None:
        self.admin = User.objects.create_user(
            email="admin@example.com",
            password="SecurePassword123!",
            role=UserRole.ADMIN,
        )
        self.customer = User.objects.create_user(
            email="customer@example.com",
            password="SecurePassword123!",
            role=UserRole.CUSTOMER,
        )

        self.stats_url = reverse("dashboard:dashboard_stats")

    def test_get_dashboard_stats_admin(self) -> None:
        """
        Back office admins can query statistics.
        """
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.stats_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("order_volumes", response.data["data"])
        self.assertIn("orders_by_status", response.data["data"])
        self.assertIn("new_customers", response.data["data"])
        self.assertIn("open_support_chats", response.data["data"])
        self.assertIn("total_delivered_revenue", response.data["data"])

    def test_get_dashboard_stats_customer_forbidden(self) -> None:
        """
        Customers should receive a forbidden error.
        """
        self.client.force_authenticate(user=self.customer)
        response = self.client.get(self.stats_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
