import uuid
from django.db import models
from django.contrib.auth import get_user_model
from apps.chats.models.conversation import Conversation

User = get_user_model()


class Message(models.Model):
    """
    Model storing specific messages inside a support conversation.
    Supports either plain text or image uploads.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages"
    )
    text = models.TextField(null=True, blank=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "chat_messages"
        ordering = ["created_at"]

    def __str__(self) -> str:
        sender_label = self.sender.email or self.sender.phone or str(self.sender.id)
        return f"Message by {sender_label} in Chat {self.conversation_id}"
