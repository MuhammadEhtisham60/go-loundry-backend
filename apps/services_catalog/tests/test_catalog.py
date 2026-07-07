from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.authentication.models.user import UserRole
from apps.services_catalog.models import Service

User = get_user_model()


class ServicesCatalogTests(APITestCase):
    """
    Test suite for laundry services catalog management and display ordering.
    """

    def setUp(self) -> None:
        self.list_url = reverse("services_catalog:service_list")
        self.reorder_url = reverse("services_catalog:service_reorder")

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

        # Create some default active and inactive services
        self.service1 = Service.objects.create(
            name="Wash & Iron",
            description="Machine wash and press",
            price=150.00,
            is_active=True,
            display_order=1,
        )
        self.service2 = Service.objects.create(
            name="Dry Cleaning",
            description="Chemical clean",
            price=300.00,
            is_active=True,
            display_order=2,
        )
        self.service3 = Service.objects.create(
            name="Blanket Wash",
            description="Heavy blanket cleaning",
            price=500.00,
            is_active=False,
            display_order=3,
        )

    def test_list_services_customer(self) -> None:
        """
        Customers should only see active services in display order.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return active ones (Wash & Iron, Dry Cleaning)
        self.assertEqual(len(response.data["data"]), 2)
        self.assertEqual(response.data["data"][0]["name"], "Wash & Iron")

    def test_list_services_admin(self) -> None:
        """
        Admins can view inactive services as well.
        """
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(f"{self.list_url}?include_inactive=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should return all 3 services
        self.assertEqual(len(response.data["data"]), 3)

    def test_create_service_unauthorized(self) -> None:
        """
        Regular customers cannot create new catalog services.
        """
        payload = {
            "name": "Shoe Cleaning",
            "unit": "PAIR",
            "price": 250.00,
        }
        self.client.force_authenticate(user=self.customer)
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_service_admin(self) -> None:
        """
        Admins can create new services.
        """
        payload = {
            "name": "Shoe Cleaning",
            "unit": "PAIR",
            "price": 250.00,
        }
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["name"], "Shoe Cleaning")
        self.assertTrue(Service.objects.filter(name="Shoe Cleaning").exists())

    def test_soft_delete_service(self) -> None:
        """
        Deleting a service sets is_deleted=True instead of purging from the database.
        """
        self.client.force_authenticate(user=self.admin)
        detail_url = reverse(
            "services_catalog:service_detail", kwargs={"pk": str(self.service1.id)}
        )
        response = self.client.delete(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Service.objects.filter(id=self.service1.id).exists())
        self.assertTrue(
            Service.all_objects.filter(id=self.service1.id).exists()
        )  # Exists in database soft-deleted

    def test_reorder_services(self) -> None:
        """
        Verify display order changes in bulk.
        """
        self.client.force_authenticate(user=self.admin)
        payload = {
            "services": [
                {"id": str(self.service1.id), "display_order": 10},
                {"id": str(self.service2.id), "display_order": 5},
            ]
        }
        response = self.client.post(self.reorder_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.service1.refresh_from_db()
        self.service2.refresh_from_db()
        self.assertEqual(self.service1.display_order, 10)
        self.assertEqual(self.service2.display_order, 5)
