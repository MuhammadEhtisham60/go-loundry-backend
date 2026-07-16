from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from apps.authentication.models.role import Role, Permission

User = get_user_model()


class TeamManagementTests(APITestCase):
    """
    Test suite verifying team invitations, complete signup flow,
    HasPermissionCode class, role CRUD validation rules.
    """

    def setUp(self) -> None:
        self.super_admin_role = Role.objects.get(name="Super Admin")
        self.admin_role = Role.objects.get(name="Admin")
        self.support_role = Role.objects.get(name="Support Agent")

        self.users_permission = Permission.objects.get(code="users")

        self.super_admin_user = User.objects.create_user(
            email="superadmin@example.com",
            password="SecurePassword123!",
            role=self.super_admin_role,
            is_active=True,
        )
        self.admin_user = User.objects.create_user(
            email="admin@example.com",
            password="SecurePassword123!",
            role=self.admin_role,
            is_active=True,
        )
        self.support_user = User.objects.create_user(
            email="support@example.com",
            password="SecurePassword123!",
            role=self.support_role,
            is_active=True,
        )

        self.user_list_url = reverse("users:user-list")
        self.user_invite_url = reverse("users:user-invite")
        self.complete_signup_url = reverse("users:user-complete-signup")
        self.role_list_url = reverse("roles-list")
        self.permission_list_url = reverse("permissions-list")

    def test_permission_enforcement_for_list_users(self) -> None:
        """
        Only users with 'users' permission (Super Admin or Admin) can view team.
        """
        # Super Admin - allowed
        self.client.force_authenticate(user=self.super_admin_user)
        response = self.client.get(self.user_list_url, {"type": "team"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Admin - forbidden (does not have 'users' permission)
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.user_list_url, {"type": "team"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Support Agent - forbidden
        self.client.force_authenticate(user=self.support_user)
        response = self.client.get(self.user_list_url, {"type": "team"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invite_and_complete_signup_flow(self) -> None:
        """
        Verify the complete back-office team invitation and registration flow.
        """
        self.client.force_authenticate(user=self.super_admin_user)
        payload = {
            "full_name": "New Team Member",
            "email": "newmember@example.com",
            "role_id": self.support_role.id,
        }

        # 1. Invite user
        response = self.client.post(self.user_invite_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("invite_token", response.data["data"])

        token = response.data["data"]["invite_token"]
        invited_user = User.objects.get(email="newmember@example.com")
        self.assertEqual(invited_user.invite_status, "pending")
        self.assertFalse(invited_user.is_active)
        self.assertEqual(invited_user.avatar_initials, "NTM")

        # 2. Complete signup (activate)
        self.client.force_authenticate(user=None)
        signup_payload = {
            "token": token,
            "password": "NewSecretPassword123!",
        }
        response = self.client.post(self.complete_signup_url, signup_payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("tokens", response.data["data"])

        invited_user.refresh_from_db()
        self.assertEqual(invited_user.invite_status, "active")
        self.assertTrue(invited_user.is_active)
        self.assertIsNotNone(invited_user.last_active)
        self.assertTrue(invited_user.check_password("NewSecretPassword123!"))

    def test_prevent_deactivating_or_deleting_last_super_admin(self) -> None:
        """
        Ensure we cannot delete or deactivate the last Super Admin.
        """
        self.client.force_authenticate(user=self.super_admin_user)
        url = reverse("users:user-detail", kwargs={"pk": str(self.super_admin_user.id)})

        # Deactivate check
        response = self.client.patch(url, {"is_active": False}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Cannot deactivate", response.data["message"])

        # Delete check
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Cannot delete", response.data["message"])

    def test_role_crud_validations(self) -> None:
        """
        Test CRUD actions on roles and deletion blocking.
        """
        self.client.force_authenticate(user=self.super_admin_user)

        # 1. Create a custom role
        payload = {
            "name": "Custom Editor",
            "permission_codes": ["pricing", "services"],
        }
        response = self.client.post(self.role_list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        role_id = response.data["data"]["id"]

        # 2. Assign to user and block deletion
        temp_user = User.objects.create_user(
            email="temp@example.com",
            password="SecurePassword123!",
            role_id=role_id,
        )
        role_url = reverse("roles-detail", kwargs={"pk": role_id})
        response = self.client.delete(role_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Cannot delete role because users are assigned", response.data["message"])

        # 3. Remove user and delete role
        temp_user.delete()
        response = self.client.delete(role_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_permission_list_endpoint(self) -> None:
        """
        Verify users with permission can read all permission items.
        """
        self.client.force_authenticate(user=self.super_admin_user)
        response = self.client.get(self.permission_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data["data"]), 0)
