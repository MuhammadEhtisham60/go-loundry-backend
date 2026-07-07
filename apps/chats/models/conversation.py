import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Conversation(models.Model):
    """
    Model representing support chat sessions.
    Links a customer to an assigned support agent and tracks resolution status.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="conversations"
    )
    assigned_agent = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_conversations",
    )
    is_resolved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "conversations"
        ordering = ["-updated_at"]

    def __str__(self) -> str:
        status_str = "Resolved" if self.is_resolved else "Active"
        return f"Chat {self.id} with {self.customer} ({status_str})"
