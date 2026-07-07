from typing import Optional, Any
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.chats.models import Conversation, Message
from apps.common.services.storage import StorageService
from apps.common.services.notifications import NotificationService

User = get_user_model()


class ChatService:
    """
    Service layer containing operations for support conversations and messages.
    Pre-wired to invoke Storage and Notification services.
    """

    @staticmethod
    def create_or_get_conversation(customer: User) -> Conversation:
        """
        Retrieves the customer's active unresolved conversation, or
        creates a new one if none is active.
        """
        conversation = Conversation.objects.filter(
            customer=customer, is_resolved=False
        ).first()

        if not conversation:
            conversation = Conversation.objects.create(customer=customer)

        return conversation

    @staticmethod
    def send_message(
        sender: User,
        conversation_id: str,
        text: Optional[str] = None,
        image_file: Optional[Any] = None,
    ) -> Message:
        """
        Appends a new text/image reply to the conversation.
        If conversation was resolved, re-opens it upon customer activity.
        """
        conversation = get_object_or_404(Conversation, id=conversation_id)

        if not text and not image_file:
            raise serializers.ValidationError(
                "Message must contain either text or an uploaded image."
            )

        # Check conversation access rights
        if sender.role == "CUSTOMER" and conversation.customer != sender:
            raise serializers.ValidationError("Access denied.")

        with transaction.atomic():
            # If resolved customer replies, re-open chat session
            if conversation.is_resolved and sender.role == "CUSTOMER":
                conversation.is_resolved = False
                conversation.save()

            image_url = None
            if image_file:
                image_url = StorageService.upload_file(image_file, folder="chats")

            message = Message.objects.create(
                conversation=conversation,
                sender=sender,
                text=text,
                image_url=image_url,
            )

            # Update conversation timestamp to float it to top of active list
            conversation.save()

        # Trigger notifications for counterparties
        if sender.role == "CUSTOMER":
            # Alert assigned agent or support pool
            if conversation.assigned_agent:
                NotificationService.send_push(
                    conversation.assigned_agent.id,
                    "New Support Message",
                    f"Message from {sender.full_name or sender.email}",
                )
        else:
            # Alert the customer
            NotificationService.send_push(
                conversation.customer.id,
                "Support Reply",
                text or "Sent an image attachment.",
            )

        return message

    @staticmethod
    def assign_agent(conversation_id: str, agent_id: str) -> Conversation:
        """
        Assigns a support agent to handle the conversation.
        """
        conversation = get_object_or_404(Conversation, id=conversation_id)
        agent = get_object_or_404(User, id=agent_id)

        if agent.role not in ["SUPPORT_AGENT", "ADMIN", "SUPER_ADMIN"]:
            raise serializers.ValidationError(
                "Assigned user must be a support agent or administrator."
            )

        conversation.assigned_agent = agent
        conversation.save()

        NotificationService.send_push(
            conversation.customer.id,
            "Agent Assigned",
            f"Support agent {agent.full_name or agent.email} has been assigned to help you.",
        )

        return conversation

    @staticmethod
    def resolve_conversation(conversation_id: str) -> Conversation:
        """
        Marks the support session as resolved.
        """
        conversation = get_object_or_404(Conversation, id=conversation_id)
        conversation.is_resolved = True
        conversation.save()

        NotificationService.send_push(
            conversation.customer.id,
            "Chat Resolved",
            "Your support chat has been marked as resolved.",
        )

        return conversation
