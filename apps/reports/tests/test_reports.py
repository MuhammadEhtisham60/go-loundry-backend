from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.authentication.models.user import UserRole

User = get_user_model()


class ReportsTests(APITestCase):
    """
    Test suite for admin-facing analytics reports.
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

        self.orders_url = reverse("reports:orders_report")
        self.revenue_url = reverse("reports:revenue_report")
        self.customers_url = reverse("reports:customer_report")
        self.services_url = reverse("reports:service_report")
        self.zones_url = reverse("reports:zone_report")

    def test_get_reports_admin_success(self) -> None:
        """
        Admins must be allowed access to all report queries.
        """
        self.client.force_authenticate(user=self.admin)

        for url in [
            self.orders_url,
            self.revenue_url,
            self.customers_url,
            self.services_url,
            self.zones_url,
        ]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_reports_customer_forbidden(self) -> None:
        """
        Customers should be rejected with a forbidden response status code.
        """
        self.client.force_authenticate(user=self.customer)

        for url in [
            self.orders_url,
            self.revenue_url,
            self.customers_url,
            self.services_url,
            self.zones_url,
        ]:
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

