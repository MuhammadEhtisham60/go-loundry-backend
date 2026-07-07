from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from decimal import Decimal
import datetime

from apps.authentication.models.user import UserRole
from apps.addresses.models import Address
from apps.services_catalog.models import Service
from apps.locations.models import WarehouseSetting, DeliveryTier
from apps.orders.models import Order, OrderStatus

User = get_user_model()


class OrdersTests(APITestCase):
    """
    Test suite for laundry order lifecycle, pricing checks, and cancellations.
    """

    def setUp(self) -> None:
        self.super_admin = User.objects.create_user(
            email="superadmin@example.com",
            password="SecurePassword123!",
            role=UserRole.SUPER_ADMIN,
        )
        self.customer = User.objects.create_user(
            email="customer@example.com",
            phone="03001234567",
            password="SecurePassword123!",
            role=UserRole.CUSTOMER,
        )

        # Setup warehouse Clifton Karachi coordinates
        self.warehouse = WarehouseSetting.objects.create(
            latitude=Decimal("24.8138"),
            longitude=Decimal("67.0336"),
            max_service_radius_km=Decimal("10.00"),
        )

        # Delivery tier 0 - 5 km = Rs.50
        DeliveryTier.objects.create(
            min_distance_km=Decimal("0.0"),
            max_distance_km=Decimal("5.0"),
            charge=Decimal("50.00"),
        )

        # Address Clifton ( ~1.5 km away )
        self.address_inside = Address.objects.create(
            user=self.customer,
            address_type="HOME",
            address_line="Clifton Area",
            latitude=Decimal("24.8050"),
            longitude=Decimal("67.0250"),
            is_default=True,
        )

        # Address Gulshan ( ~12 km away )
        self.address_outside = Address.objects.create(
            user=self.customer,
            address_type="OFFICE",
            address_line="Gulshan Area",
            latitude=Decimal("24.9180"),
            longitude=Decimal("67.0970"),
        )

        # Catalog Services
        self.service = Service.objects.create(
            name="Wash & Iron",
            description="Machine Wash",
            price=Decimal("150.00"),
            is_active=True,
        )

        self.list_url = reverse("orders:order_list")

        self.client.force_authenticate(user=self.customer)

    def test_place_order_success(self) -> None:
        """
        Verify successful order placement with correct fee calculations.
        """
        payload = {
            "pickup_address_id": str(self.address_inside.id),
            "pickup_date": str(datetime.date.today() + datetime.timedelta(days=1)),
            "pickup_slot": "MORNING",
            "special_instructions": "Handle with care",
            "items": [{"service_id": str(self.service.id), "quantity": 2.0}],
        }

        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        order_id = response.data["data"]["id"]
        order = Order.objects.get(id=order_id)

        # 2 * 150 (service) + 50 (delivery) = 350
        self.assertEqual(order.total_services_amount, Decimal("300.00"))
        self.assertEqual(order.total_amount, Decimal("350.00"))
        self.assertEqual(order.delivery_charge, Decimal("50.00"))

    def test_place_order_outside_radius_fails(self) -> None:
        """
        Placing an order outside warehouse coverage range should fail.
        """
        payload = {
            "pickup_address_id": str(self.address_outside.id),
            "pickup_date": str(datetime.date.today() + datetime.timedelta(days=1)),
            "pickup_slot": "MORNING",
            "items": [{"service_id": str(self.service.id), "quantity": 1.0}],
        }

        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["message"],
            "Validation failed",
        )
        self.assertIn(
            "We are not in your area yet! Coming soon to your neighbourhood",
            str(response.data["errors"]),
        )


    def test_cancel_order_placed_stage(self) -> None:
        """
        Verify customer can cancel order when it's still in the placed state.
        """
        order = Order.objects.create(
            user=self.customer,
            pickup_address=self.address_inside,
            address_line_snapshot=self.address_inside.address_line,
            latitude=self.address_inside.latitude,
            longitude=self.address_inside.longitude,
            distance_km=Decimal("1.5"),
            delivery_charge=Decimal("50.00"),
            total_services_amount=Decimal("150.00"),
            total_amount=Decimal("200.00"),
            pickup_date=datetime.date.today(),
            pickup_slot="MORNING",
        )

        cancel_url = reverse("orders:order_cancel", kwargs={"pk": str(order.id)})
        payload = {"reason": "Changed my plans"}

        response = self.client.post(cancel_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        order.refresh_from_db()
        self.assertEqual(order.status, OrderStatus.CANCELLED)
        self.assertEqual(order.cancellation_reason, "Changed my plans")

    def test_cancel_order_after_confirmed_fails(self) -> None:
        """
        Verify customer cannot cancel order once it is confirmed by the admin.
        """
        order = Order.objects.create(
            user=self.customer,
            status=OrderStatus.ORDER_CONFIRMED,
            pickup_address=self.address_inside,
            address_line_snapshot=self.address_inside.address_line,
            latitude=self.address_inside.latitude,
            longitude=self.address_inside.longitude,
            distance_km=Decimal("1.5"),
            delivery_charge=Decimal("50.00"),
            total_services_amount=Decimal("150.00"),
            total_amount=Decimal("200.00"),
            pickup_date=datetime.date.today(),
            pickup_slot="MORNING",
        )

        cancel_url = reverse("orders:order_cancel", kwargs={"pk": str(order.id)})
        payload = {"reason": "Changed my plans"}

        response = self.client.post(cancel_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        order.refresh_from_db()
        self.assertEqual(order.status, OrderStatus.ORDER_CONFIRMED)
