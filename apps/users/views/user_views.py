from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.users.services import UserManagementService
from apps.users.selectors import UserSelector
from apps.users.serializers import (
    CustomerListSerializer,
    CustomerDetailSerializer,
    BlockUserSerializer,
)
from apps.users.permissions import IsAdmin, IsSupportAgent
from common.responses.standard import StandardResponse


class CustomerListView(APIView):
    """
    API View to view and search customer records.
    Accessible to Support Agents, Admins, and Super Admins.
    """

    permission_classes = [IsAuthenticated, IsSupportAgent]

    def get(self, request: Request) -> Response:
        search = request.query_params.get("search")
        is_blocked_str = request.query_params.get("is_blocked")

        is_blocked = None
        if is_blocked_str is not None:
            is_blocked = is_blocked_str.lower() == "true"

        customers = UserSelector.get_customers(
            search_query=search, is_blocked=is_blocked
        )
        serializer = CustomerListSerializer(customers, many=True)

        return StandardResponse(
            data=serializer.data,
            message="Customer records list retrieved.",
            status=status.HTTP_200_OK,
        )


class CustomerDetailView(APIView):
    """
    API View to view a customer profile, saved addresses, and their order history.
    Accessible to Support Agents, Admins, and Super Admins.
    """

    permission_classes = [IsAuthenticated, IsSupportAgent]

    def get(self, request: Request, pk: str) -> Response:
        customer = UserSelector.get_customer_by_id(pk)
        if not customer:
            return StandardResponse(
                data=None,
                message="Customer not found.",
                status=status.HTTP_404_NOT_FOUND,
                success=False,
            )

        serializer = CustomerDetailSerializer(customer)
        return StandardResponse(
            data=serializer.data,
            message="Customer details retrieved.",
            status=status.HTTP_200_OK,
        )


class CustomerBlockView(APIView):
    """
    API View to block or unblock a customer account.
    Restricted to Admins and Super Admins only (Support Agents cannot block).
    """

    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request: Request, pk: str) -> Response:
        serializer = BlockUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = UserManagementService.set_block_status(
            user_id=pk, is_blocked=serializer.validated_data["is_blocked"]
        )

        message = (
            "Customer account blocked successfully."
            if user.is_blocked
            else "Customer account unblocked successfully."
        )

        return StandardResponse(
            data=CustomerListSerializer(user).data,
            message=message,
            status=status.HTTP_200_OK,
        )
