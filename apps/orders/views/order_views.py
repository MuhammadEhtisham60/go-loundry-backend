from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.orders.services import OrderService
from apps.orders.selectors import OrderSelector
from apps.orders.serializers import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderCancelSerializer,
    OrderStatusUpdateSerializer,
    OrderReorderSerializer,
)
from apps.orders.permissions import IsCustomer, IsSupportAgent
from common.responses.standard import StandardResponse


class OrderListView(APIView):
    """
    API View to list and place laundry orders.
    Requires authentication.
    """

    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsCustomer()]
        return [IsAuthenticated()]

    def get(self, request: Request) -> Response:
        status_filter = request.query_params.get("status")
        date_from = request.query_params.get("date_from")
        date_to = request.query_params.get("date_to")
        customer_id = request.query_params.get("customer_id")

        orders = OrderSelector.list_orders(
            user=request.user,
            status_value=status_filter,
            date_from=date_from,
            date_to=date_to,
            customer_id=customer_id,
        )
        serializer = OrderSerializer(orders, many=True)
        return StandardResponse(
            data=serializer.data,
            message="Orders list retrieved successfully.",
            status=status.HTTP_200_OK,
        )

    def post(self, request: Request) -> Response:
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = OrderService.create_order(
            user=request.user, validated_data=serializer.validated_data
        )
        result_serializer = OrderSerializer(order)

        return StandardResponse(
            data=result_serializer.data,
            message="Order placed successfully.",
            status=status.HTTP_201_CREATED,
        )


class OrderDetailView(APIView):
    """
    API View to view order details.
    Customers can only view their own; Admins/Support can view any.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request: Request, pk: str) -> Response:
        order = OrderSelector.get_order_by_id(order_id=pk, user=request.user)
        if not order:
            return StandardResponse(
                data=None,
                message="Order not found.",
                status=status.HTTP_404_NOT_FOUND,
                success=False,
            )

        serializer = OrderSerializer(order)
        return StandardResponse(
            data=serializer.data,
            message="Order details retrieved successfully.",
            status=status.HTTP_200_OK,
        )


class OrderCancelView(APIView):
    """
    API View to cancel an order.
    Requires authentication. Customers can only cancel placed orders.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request: Request, pk: str) -> Response:
        serializer = OrderCancelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = OrderService.cancel_order(
            user=request.user,
            order_id=pk,
            reason=serializer.validated_data["reason"],
        )

        return StandardResponse(
            data=OrderSerializer(order).data,
            message="Order cancelled successfully.",
            status=status.HTTP_200_OK,
        )


class OrderStatusUpdateView(APIView):
    """
    API View for back office admin/support to update status and rider details.
    """

    permission_classes = [IsAuthenticated, IsSupportAgent]

    def put(self, request: Request, pk: str) -> Response:
        serializer = OrderStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        extra_data = {
            "rider_name": serializer.validated_data.get("rider_name"),
            "rider_contact": serializer.validated_data.get("rider_contact"),
            "admin_notes": serializer.validated_data.get("admin_notes"),
        }

        # Filter out None values
        extra_data = {k: v for k, v in extra_data.items() if v is not None}

        order = OrderService.update_order_status(
            order_id=pk,
            status_value=serializer.validated_data["status"],
            extra_data=extra_data,
        )

        return StandardResponse(
            data=OrderSerializer(order).data,
            message="Order status updated successfully.",
            status=status.HTTP_200_OK,
        )


class OrderReorderView(APIView):
    """
    API View to re-checkout all services from a previous order.
    Restricted to Customers.
    """

    permission_classes = [IsAuthenticated, IsCustomer]

    def post(self, request: Request, pk: str) -> Response:
        serializer = OrderReorderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = OrderService.reorder(
            user=request.user,
            order_id=pk,
            pickup_date=serializer.validated_data["pickup_date"],
            pickup_slot=serializer.validated_data["pickup_slot"],
        )

        return StandardResponse(
            data=OrderSerializer(order).data,
            message="Reordered successfully.",
            status=status.HTTP_201_CREATED,
        )
