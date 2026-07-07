from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.authentication.models.user import UserRole
from apps.chats.models import Conversation, Message

User = get_user_model()


class ChatsTests(APITestCase):
    """
    Test suite for support chat conversations and messages.
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
            password="SecurePassword123!",
            role=UserRole.CUSTOMER,
        )

        self.list_url = reverse("chats:conversation_list")
        self.client.force_authenticate(user=self.customer)

    def test_start_conversation_success(self) -> None:
        """
        Verify creating a new active conversation for a customer.
        """
        response = self.client.post(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["data"]["is_resolved"])
        self.assertEqual(
            response.data["data"]["customer"]["email"], "customer@example.com"
        )

    def test_send_message_success(self) -> None:
        """
        Verify user can append messages to an initialized chat.
        """
        conv = Conversation.objects.create(customer=self.customer)
        msg_url = reverse(
            "chats:message_list", kwargs={"conversation_id": str(conv.id)}
        )

        payload = {"text": "Hello support team!"}
        response = self.client.post(msg_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["text"], "Hello support team!")
        self.assertEqual(response.data["data"]["sender"]["email"], "customer@example.com")

    def test_assign_agent_and_resolve_admin(self) -> None:
        """
        Admins/Support can assign agents and resolve chat sessions.
        """
        conv = Conversation.objects.create(customer=self.customer)

        assign_url = reverse(
            "chats:conversation_assign", kwargs={"conversation_id": str(conv.id)}
        )
        resolve_url = reverse(
            "chats:conversation_resolve", kwargs={"conversation_id": str(conv.id)}
        )

        # Customer role cannot assign
        payload = {"agent_id": str(self.support.id)}
        response = self.client.post(assign_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin role can assign
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(assign_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["data"]["assigned_agent"]["email"], "support@example.com"
        )

        # Admin resolves
        response = self.client.post(resolve_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["data"]["is_resolved"])
