from rest_framework import serializers
from apps.chats.models import Conversation, Message
from apps.authentication.serializers import UserSerializer


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer representing customer support chat sessions.
    """

    customer = UserSerializer(read_only=True)
    assigned_agent = UserSerializer(read_only=True)

    class Meta:
        model = Conversation
        fields = ("id", "customer", "assigned_agent", "is_resolved", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer representing chat messages.
    """

    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ("id", "conversation", "sender", "text", "image_url", "created_at")
        read_only_fields = ("id", "conversation", "sender", "created_at")


class MessageInputSerializer(serializers.Serializer):
    """
    Validator for incoming customer replies or image uploads.
    """

    text = serializers.CharField(required=False, allow_blank=True, default=None)
    image = serializers.FileField(required=False, allow_null=True, default=None)


class AssignAgentSerializer(serializers.Serializer):
    """
    Validator for assigning agents to chat sessions.
    """

    agent_id = serializers.UUIDField(required=True)
