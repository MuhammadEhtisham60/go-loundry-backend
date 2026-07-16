from rest_framework import serializers
from apps.locations.models import WarehouseSetting, DeliveryTier


class WarehouseSettingSerializer(serializers.ModelSerializer):
    """
    Serializer for Warehouse Setting configuration.
    """

    class Meta:
        model = WarehouseSetting
        fields = ("id", "latitude", "longitude", "max_service_radius_km", "address")


class DeliveryTierSerializer(serializers.ModelSerializer):
    """
    Serializer for Delivery Fee Tier settings.
    """

    class Meta:
        model = DeliveryTier
        fields = ("id", "min_distance_km", "max_distance_km", "charge")

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # Rename keys for frontend
        ret["from"] = float(ret.pop("min_distance_km"))
        ret["to"] = float(ret.pop("max_distance_km"))
        ret["charge"] = float(ret["charge"])
        return ret

    def to_internal_value(self, data):
        # Map frontend keys back to model fields
        data_copy = data.copy() if hasattr(data, 'copy') else dict(data)
        if "from" in data_copy:
            data_copy["min_distance_km"] = data_copy.pop("from")
        if "to" in data_copy:
            data_copy["max_distance_km"] = data_copy.pop("to")
        return super().to_internal_value(data_copy)


class ValidateAreaSerializer(serializers.Serializer):
    """
    Serializer to validate user GPS coordinates for service area coverage.
    """

    latitude = serializers.FloatField(required=True)
    longitude = serializers.FloatField(required=True)
