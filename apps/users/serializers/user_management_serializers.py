from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.addresses.serializers import AddressSerializer

User = get_user_model()


class CustomerListSerializer(serializers.ModelSerializer):
    """
    Serializer representing the customer list items inside admin pages.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone",
            "full_name",
            "profile_photo",
            "is_blocked",
            "created_at",
        )


class CustomerDetailSerializer(serializers.ModelSerializer):
    """
    Serializer representing comprehensive customer detail info,
    including addresses and order histories.
    """

    addresses = AddressSerializer(many=True, read_only=True)
    orders = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone",
            "full_name",
            "profile_photo",
            "is_blocked",
            "created_at",
            "addresses",
            "orders",
        )

    def get_orders(self, obj) -> list:
        # Dynamic import to avoid circular dependencies with the orders module
        from apps.orders.models import Order
        from apps.orders.serializers import OrderSerializer

        orders = Order.objects.filter(user=obj)
        return OrderSerializer(orders, many=True).data


class BlockUserSerializer(serializers.Serializer):
    """
    Validation payload for blocking or unblocking customer accounts.
    """

    is_blocked = serializers.BooleanField(required=True)
