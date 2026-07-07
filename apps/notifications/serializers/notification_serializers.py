from rest_framework import serializers
from apps.notifications.models import NotificationLog


class NotificationLogSerializer(serializers.ModelSerializer):
    """
    Serializer representing log history entries.
    """

    class Meta:
        model = NotificationLog
        fields = ("id", "title", "body", "notification_type", "is_sent", "created_at")
        read_only_fields = fields
