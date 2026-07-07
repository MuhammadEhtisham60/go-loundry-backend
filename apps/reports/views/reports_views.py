import datetime
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.reports.selectors import ReportsSelector
from apps.authentication.permissions import IsAdmin
from common.responses.standard import StandardResponse


class OrdersReportView(APIView):
    """
    API View to generate order metrics reports.
    Restricted to Admins and Super Admins.
    """

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request: Request) -> Response:
        # Default to past 30 days if not provided
        today = datetime.date.today()
        thirty_days_ago = today - datetime.timedelta(days=30)

        date_from = request.query_params.get("date_from", str(thirty_days_ago))
        date_to = request.query_params.get("date_to", str(today))

        data = ReportsSelector.get_orders_report(date_from, date_to)
        return StandardResponse(
            data=data,
            message="Orders report compiled successfully.",
            status=status.HTTP_200_OK,
        )


class RevenueReportView(APIView):
    """
    API View to generate revenue reports from delivered orders.
    Restricted to Admins and Super Admins.
    """

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request: Request) -> Response:
        today = datetime.date.today()
        thirty_days_ago = today - datetime.timedelta(days=30)

        date_from = request.query_params.get("date_from", str(thirty_days_ago))
        date_to = request.query_params.get("date_to", str(today))

        data = ReportsSelector.get_revenue_report(date_from, date_to)
        return StandardResponse(
            data=data,
            message="Revenue report compiled successfully.",
            status=status.HTTP_200_OK,
        )


class CustomerReportView(APIView):
    """
    API View to retrieve customer signup metrics and status logs.
    Restricted to Admins and Super Admins.
    """

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request: Request) -> Response:
        data = ReportsSelector.get_customer_report()
        return StandardResponse(
            data=data,
            message="Customer analytics report compiled.",
            status=status.HTTP_200_OK,
        )


class ServicePopularityReportView(APIView):
    """
    API View to retrieve popularity statistics for services.
    Restricted to Admins and Super Admins.
    """

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request: Request) -> Response:
        data = ReportsSelector.get_service_popularity_report()
        return StandardResponse(
            data=data,
            message="Service popularity report compiled.",
            status=status.HTTP_200_OK,
        )


class ZoneReportView(APIView):
    """
    API View to analyze geographical orders and revenues by distance bands.
    Restricted to Admins and Super Admins.
    """

    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request: Request) -> Response:
        data = ReportsSelector.get_zone_report()
        return StandardResponse(
            data=data,
            message="Geographical zone report compiled.",
            status=status.HTTP_200_OK,
        )
