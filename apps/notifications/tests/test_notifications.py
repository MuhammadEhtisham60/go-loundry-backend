from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.authentication.models.user import UserRole
from apps.notifications.models import NotificationLog

User = get_user_model()


class NotificationsTests(APITestCase):
    """
    Test suite for customer notification history.
    """

    def setUp(self) -> None:
        self.customer = User.objects.create_user(
            email="customer@example.com",
            password="SecurePassword123!",
            role=UserRole.CUSTOMER,
        )
        self.other_customer = User.objects.create_user(
            email="other@example.com",
            password="SecurePassword123!",
            role=UserRole.CUSTOMER,
        )

        # Create some notifications
        NotificationLog.objects.create(
            user=self.customer,
            title="Welcome to GoLaundry",
            body="Thanks for signing up!",
            notification_type="PUSH",
        )
        NotificationLog.objects.create(
            user=self.customer,
            title="Order Received",
            body="We have received your order.",
            notification_type="SMS",
        )
        # Notification for other user
        NotificationLog.objects.create(
            user=self.other_customer,
            title="Other Notification",
            body="Other details",
            notification_type="PUSH",
        )

        self.list_url = reverse("notifications:notification_list")

    def test_list_notifications_authenticated(self) -> None:
        """
        An authenticated customer should only retrieve their own notification logs.
        """
        self.client.force_authenticate(user=self.customer)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return only the 2 notifications for this customer
        self.assertEqual(len(response.data["data"]), 2)
        self.assertEqual(response.data["data"][0]["title"], "Order Received")  # Ordered by -created_at
        self.assertEqual(response.data["data"][1]["title"], "Welcome to GoLaundry")

    def test_list_notifications_unauthenticated_fails(self) -> None:
        """
        Unauthenticated requests to read notification histories must be blocked.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
