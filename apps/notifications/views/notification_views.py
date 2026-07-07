from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.notifications.selectors import NotificationSelector
from apps.notifications.serializers import NotificationLogSerializer
from common.responses.standard import StandardResponse


class NotificationListView(APIView):
    """
    API View to retrieve the notification log history for the authenticated user.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        logs = NotificationSelector.get_user_notifications(request.user)
        serializer = NotificationLogSerializer(logs, many=True)
        return StandardResponse(
            data=serializer.data,
            message="Notification logs retrieved.",
            status=status.HTTP_200_OK,
        )
