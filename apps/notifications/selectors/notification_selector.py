from django.db.models import QuerySet
from django.contrib.auth import get_user_model

from apps.notifications.models import NotificationLog

User = get_user_model()


class NotificationSelector:
    """
    Selectors encapsulating read operations for dispatch logs.
    """

    @staticmethod
    def get_user_notifications(user: User) -> QuerySet:
        """
        Retrieves notification history for a user.
        """
        return NotificationLog.objects.filter(user=user)
