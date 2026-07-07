from rest_framework import serializers
from apps.locations.models import WarehouseSetting, DeliveryTier


class WarehouseSettingSerializer(serializers.ModelSerializer):
    """
    Serializer for Warehouse Setting configuration.
    """

    class Meta:
        model = WarehouseSetting
        fields = ("latitude", "longitude", "max_service_radius_km")


class DeliveryTierSerializer(serializers.ModelSerializer):
    """
    Serializer for Delivery Fee Tier settings.
    """

    class Meta:
        model = DeliveryTier
        fields = ("id", "min_distance_km", "max_distance_km", "charge")


class ValidateAreaSerializer(serializers.Serializer):
    """
    Serializer to validate user GPS coordinates for service area coverage.
    """

    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)
