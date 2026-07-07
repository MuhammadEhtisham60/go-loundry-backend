from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from decimal import Decimal
import datetime

from apps.authentication.models.user import UserRole
from apps.orders.models import Order, OrderStatus
from apps.reviews.models import Review

User = get_user_model()


class ReviewsTests(APITestCase):
    """
    Test suite for customer order rating operations.
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

        # Delivered order owned by customer
        self.order_delivered = Order.objects.create(
            user=self.customer,
            status=OrderStatus.DELIVERED,
            distance_km=Decimal("1.5"),
            delivery_charge=Decimal("50.00"),
            total_services_amount=Decimal("150.00"),
            total_amount=Decimal("200.00"),
            pickup_date=datetime.date.today(),
            pickup_slot="MORNING",
            latitude=Decimal("24.8105"),
            longitude=Decimal("67.0310"),
            address_line_snapshot="Suite 14, Block 5, Clifton, Karachi"
        )

        # Placed order owned by customer
        self.order_placed = Order.objects.create(
            user=self.customer,
            status=OrderStatus.ORDER_PLACED,
            distance_km=Decimal("1.5"),
            delivery_charge=Decimal("50.00"),
            total_services_amount=Decimal("150.00"),
            total_amount=Decimal("200.00"),
            pickup_date=datetime.date.today(),
            pickup_slot="MORNING",
            latitude=Decimal("24.8105"),
            longitude=Decimal("67.0310"),
            address_line_snapshot="Suite 14, Block 5, Clifton, Karachi"
        )


        self.list_url = reverse("reviews:review_list")
        self.client.force_authenticate(user=self.customer)

    def test_review_delivered_order_success(self) -> None:
        """
        Verify successful rating submission for a completed order.
        """
        payload = {
            "order_id": str(self.order_delivered.id),
            "rating": 5,
            "remarks": "Excellent service!",
        }

        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["rating"], 5)
        self.assertEqual(response.data["data"]["remarks"], "Excellent service!")

    def test_review_uncompleted_order_fails(self) -> None:
        """
        Submitting reviews on uncompleted (e.g. placed) orders should fail.
        """
        payload = {
            "order_id": str(self.order_placed.id),
            "rating": 4,
            "remarks": "Decent",
        }

        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Validation failed")
        self.assertIn(
            "Reviews are only allowed for delivered orders.",
            str(response.data["errors"]),
        )

    def test_review_other_user_order_fails(self) -> None:
        """
        Submitting ratings for orders owned by other users should be rejected.
        """
        self.client.force_authenticate(user=self.other_customer)
        payload = {
            "order_id": str(self.order_delivered.id),
            "rating": 4,
        }

        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Validation failed")
        self.assertIn(
            "You can only rate your own orders.",
            str(response.data["errors"]),
        )

    def test_duplicate_review_fails(self) -> None:
        """
        Ensure customers cannot submit multiple reviews for a single order.
        """
        Review.objects.create(
            user=self.customer, order=self.order_delivered, rating=5, remarks="Nice"
        )

        payload = {
            "order_id": str(self.order_delivered.id),
            "rating": 4,
        }

        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Validation failed")
        self.assertIn(
            "You have already reviewed this order.",
            str(response.data["errors"]),
        )

