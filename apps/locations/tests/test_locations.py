from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from decimal import Decimal

from apps.authentication.models.user import UserRole
from apps.locations.models import WarehouseSetting, DeliveryTier

User = get_user_model()


class LocationsTests(APITestCase):
    """
    Test suite for location settings, distance coverage, and shipping calculation endpoints.
    """

    def setUp(self) -> None:
        self.warehouse_url = reverse("locations:warehouse_setting")
        self.tiers_url = reverse("locations:tiers")
        self.validate_url = reverse("locations:validate_area")

        self.super_admin = User.objects.create_user(
            email="superadmin@example.com",
            password="SecurePassword123!",
            role=UserRole.SUPER_ADMIN,
        )
        self.customer = User.objects.create_user(
            email="customer@example.com",
            password="SecurePassword123!",
            role=UserRole.CUSTOMER,
        )

        # Create warehouse setting (Karachi Clifton area)
        self.warehouse = WarehouseSetting.objects.create(
            latitude=Decimal("24.8138"),
            longitude=Decimal("67.0336"),
            max_service_radius_km=Decimal("15.00"),
        )

        # Create a delivery tier: 0 to 5 KM = Rs.50
        self.tier = DeliveryTier.objects.create(
            min_distance_km=Decimal("0.0"),
            max_distance_km=Decimal("5.0"),
            charge=Decimal("50.00"),
        )

    def test_get_warehouse_public(self) -> None:
        """
        Any user can read the warehouse location configurations.
        """
        response = self.client.get(self.warehouse_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["data"]["latitude"], f"{self.warehouse.latitude:.6f}"
        )

    def test_update_warehouse_unauthorized(self) -> None:
        """
        Updating the warehouse location requires authentication and admin privileges.
        """
        payload = {"latitude": 24.85, "longitude": 67.02, "max_service_radius_km": 20.0}
        response = self.client.put(self.warehouse_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Customer role should fail
        self.client.force_authenticate(user=self.customer)
        response = self.client.put(self.warehouse_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_warehouse_superadmin(self) -> None:
        """
        Super Admin can successfully update the warehouse settings.
        """
        self.client.force_authenticate(user=self.super_admin)
        payload = {
            "latitude": 24.8220,
            "longitude": 67.0420,
            "max_service_radius_km": 10.00,
        }
        response = self.client.put(self.warehouse_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["data"]["latitude"], f"{payload['latitude']:.6f}"
        )

        self.assertEqual(
            float(response.data["data"]["max_service_radius_km"]),
            payload["max_service_radius_km"],
        )

    def test_validate_service_area_inside(self) -> None:
        """
        Verify coordinate within operational radius calculates distance and tier charge.
        """
        # Clifton beach Karachi is ~1.5 km away from Clifton
        payload = {"latitude": 24.8050, "longitude": 67.0250}
        response = self.client.post(self.validate_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["data"]["is_valid"])
        self.assertLess(response.data["data"]["distance_km"], 5.0)
        self.assertEqual(float(response.data["data"]["delivery_charge"]), 50.0)

    def test_validate_service_area_outside(self) -> None:
        """
        Verify coordinate outside operational radius returns is_valid=False.
        """
        # Lahore is 1000km away
        payload = {"latitude": 31.5204, "longitude": 74.3587}
        response = self.client.post(self.validate_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["data"]["is_valid"])
        self.assertEqual(float(response.data["data"]["delivery_charge"]), 0.0)
