from typing import Optional, List
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.chats.models import Conversation, Message

User = get_user_model()


class ChatSelector:
    """
    Selectors encapsulating read operations for support conversations.
    """

    @staticmethod
    def get_conversations(
        user: User, is_resolved: Optional[bool] = None
    ) -> QuerySet:
        """
        Lists conversations. Customers see only their own.
        Admins and Support see all.
        """
        queryset = Conversation.objects.select_related("customer", "assigned_agent")

        if user.role == "CUSTOMER":
            queryset = queryset.filter(customer=user)

        if is_resolved is not None:
            queryset = queryset.filter(is_resolved=is_resolved)

        return queryset

    @staticmethod
    def get_messages(user: User, conversation_id: str) -> QuerySet:
        """
        Retrieves the full message history for a conversation.
        """
        conversation = get_object_or_404(Conversation, id=conversation_id)

        # Access check
        if user.role == "CUSTOMER" and conversation.customer != user:
            raise serializers.ValidationError("Access denied.")

        return Message.objects.filter(conversation=conversation).select_related(
            "sender"
        )
