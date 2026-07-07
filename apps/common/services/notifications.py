import logging
from typing import Any

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Mock implementation for SMS and Push notifications.
    Pre-configured for future Twilio, NdLoop, and Firebase Cloud Messaging (FCM) hooks.
    """

    @staticmethod
    def send_push(user_id: Any, title: str, body: str) -> bool:
        """
        Sends a Firebase Cloud Messaging push notification.
        Placeholder implementation logging to stdout.
        """
        logger.info(f"[FCM PUSH] User: {user_id} | Title: {title} | Body: {body}")
        # Insert database log logging in actual app
        from apps.notifications.models import NotificationLog
        NotificationLog.objects.create(
            user_id=user_id,
            title=title,
            body=body,
            notification_type="PUSH",
            is_sent=True
        )
        return True

    @staticmethod
    def send_sms(phone: str, message: str) -> bool:
        """
        Sends an SMS via Twilio or NdLoop (Pakistan).
        Placeholder implementation logging to stdout.
        """
        logger.info(f"[SMS ALERT] Phone: {phone} | Msg: {message}")
        # Insert database log if user exists
        from django.contrib.auth import get_user_model
        from apps.notifications.models import NotificationLog
        User = get_user_model()
        user = User.objects.filter(phone=phone).first()
        if user:
            NotificationLog.objects.create(
                user=user,
                title="SMS Alert",
                body=message,
                notification_type="SMS",
                is_sent=True
            )
        return True
