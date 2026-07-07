from rest_framework import serializers
from apps.services_catalog.models import Service


class ServiceSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for laundry services representation.
    """

    unit_display = serializers.CharField(source="get_unit_display", read_only=True)

    class Meta:
        model = Service
        fields = (
            "id",
            "name",
            "description",
            "unit",
            "unit_display",
            "price",
            "is_active",
            "display_order",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class ReorderServiceItemSerializer(serializers.Serializer):
    """
    Validation layout for single service reorder mapping.
    """

    id = serializers.UUIDField(required=True)
    display_order = serializers.IntegerField(required=True)


class ReorderServiceListSerializer(serializers.Serializer):
    """
    Validation layout for bulk services display sequence reordering.
    """

    services = ReorderServiceItemSerializer(many=True, required=True)
