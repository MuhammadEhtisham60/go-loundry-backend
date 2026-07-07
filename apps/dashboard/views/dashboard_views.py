from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.dashboard.selectors import DashboardSelector
from apps.authentication.permissions import IsSupportAgent
from common.responses.standard import StandardResponse


class DashboardStatsView(APIView):
    """
    API View to retrieve aggregate dashboard metrics for operations management.
    Requires user to be a Support Agent, Admin, or Super Admin.
    """

    permission_classes = [IsAuthenticated, IsSupportAgent]

    def get(self, request: Request) -> Response:
        stats = DashboardSelector.get_dashboard_stats()
        return StandardResponse(
            data=stats,
            message="Dashboard statistics compiled.",
            status=status.HTTP_200_OK,
        )
