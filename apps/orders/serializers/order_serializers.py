from rest_framework import serializers
from apps.orders.models import Order, OrderItem, OrderStatus, PickupSlot
from apps.services_catalog.serializers import ServiceSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying specific service items inside an order.
    """

    service = ServiceSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "service", "quantity", "unit_price", "total_price")


class OrderSerializer(serializers.ModelSerializer):
    """
    Detailed Order model serializer showing customer profile info,
    snapshots of delivery coordinates, timing slots, and assigned riders.
    """

    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    pickup_slot_display = serializers.CharField(source="get_pickup_slot_display", read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "user",
            "status",
            "status_display",
            "pickup_address",
            "address_line_snapshot",
            "latitude",
            "longitude",
            "distance_km",
            "delivery_charge",
            "total_services_amount",
            "total_amount",
            "pickup_date",
            "pickup_slot",
            "pickup_slot_display",
            "special_instructions",
            "payment_method",
            "rider_name",
            "rider_contact",
            "admin_notes",
            "cancellation_reason",
            "created_at",
            "updated_at",
            "items",
        )
        read_only_fields = ("id", "user", "created_at", "updated_at")


class OrderItemInputSerializer(serializers.Serializer):
    """
    Validator for single catalog service checked out.
    """

    service_id = serializers.UUIDField(required=True)
    quantity = serializers.FloatField(required=True, min_value=0.1)


class OrderCreateSerializer(serializers.Serializer):
    """
    Validator for order placement payloads.
    """

    pickup_address_id = serializers.UUIDField(required=True)
    pickup_date = serializers.DateField(required=True)
    pickup_slot = serializers.ChoiceField(choices=PickupSlot.choices, required=True)
    special_instructions = serializers.CharField(
        required=False, allow_blank=True, default=""
    )
    items = OrderItemInputSerializer(many=True, required=True)

    def validate_items(self, value):
        if len(value) == 0:
            raise serializers.ValidationError("An order must contain at least one item.")
        return value


class OrderCancelSerializer(serializers.Serializer):
    """
    Validator for cancellation reasons.
    """

    reason = serializers.CharField(required=True, min_length=5)


class OrderStatusUpdateSerializer(serializers.Serializer):
    """
    Validator for back-office admin status updates and rider mapping.
    """

    status = serializers.ChoiceField(choices=OrderStatus.choices, required=True)
    rider_name = serializers.CharField(required=False, allow_blank=True)
    rider_contact = serializers.CharField(required=False, allow_blank=True)
    admin_notes = serializers.CharField(required=False, allow_blank=True)


class OrderReorderSerializer(serializers.Serializer):
    """
    Validator to re-checkout previous order items with new slots.
    """

    pickup_date = serializers.DateField(required=True)
    pickup_slot = serializers.ChoiceField(choices=PickupSlot.choices, required=True)
