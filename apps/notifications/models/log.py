import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class NotificationType(models.TextChoices):
    PUSH = "PUSH", "Push Notification"
    SMS = "SMS", "SMS"


class NotificationLog(models.Model):
    """
    Model logging dispatched alerts.
    Pre-configured for tracking message receipts.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notification_logs"
    )
    title = models.CharField(max_length=255)
    body = models.TextField()
    notification_type = models.CharField(
        max_length=20, choices=NotificationType.choices, default=NotificationType.PUSH
    )
    is_sent = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notification_logs"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.get_notification_type_display()} - {self.title} to User {self.user_id}"
