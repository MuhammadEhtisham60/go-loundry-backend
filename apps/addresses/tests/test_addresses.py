from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from decimal import Decimal

from apps.authentication.models.user import UserRole
from apps.addresses.models import Address

User = get_user_model()


class AddressesTests(APITestCase):
    """
    Test suite for saved customer addresses operations.
    """

    def setUp(self) -> None:
        self.list_url = reverse("addresses:address_list")

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

        self.client.force_authenticate(user=self.customer)

    def test_create_first_address_auto_default(self) -> None:
        """
        The first address a user creates should automatically be marked is_default=True.
        """
        payload = {
            "address_type": "HOME",
            "address_line": "123 Street, Clifton, Karachi",
            "latitude": 24.8100,
            "longitude": 67.0300,
            "is_default": False,  # Sent as False, should be overwritten to True
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data["data"]["is_default"])

    def test_default_rotation(self) -> None:
        """
        Setting a new address as default should clear default flags on previous addresses.
        """
        # Create address 1
        addr1 = Address.objects.create(
            user=self.customer,
            address_type="HOME",
            address_line="Address One",
            latitude=Decimal("24.8"),
            longitude=Decimal("67.0"),
            is_default=True,
        )

        # Create address 2 marked default
        payload = {
            "address_type": "OFFICE",
            "address_line": "Address Two",
            "latitude": 24.82,
            "longitude": 67.04,
            "is_default": True,
        }
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify new is default, old is not
        addr1.refresh_from_db()
        self.assertFalse(addr1.is_default)
        self.assertTrue(response.data["data"]["is_default"])

    def test_delete_default_rotates_default_to_newest(self) -> None:
        """
        Deleting the default address should make the remaining newest address default.
        """
        addr1 = Address.objects.create(
            user=self.customer,
            address_type="HOME",
            address_line="Address One",
            latitude=Decimal("24.8"),
            longitude=Decimal("67.0"),
            is_default=False,
        )
        addr2 = Address.objects.create(
            user=self.customer,
            address_type="OFFICE",
            address_line="Address Two",
            latitude=Decimal("24.82"),
            longitude=Decimal("67.04"),
            is_default=True,
        )

        # Delete addr2 (default)
        detail_url = reverse(
            "addresses:address_detail", kwargs={"pk": str(addr2.id)}
        )
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify addr1 is now default
        addr1.refresh_from_db()
        self.assertTrue(addr1.is_default)
