from rest_framework import serializers
from apps.addresses.models import Address


class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer representing saved physical customer addresses.
    Validates GPS coordinates formats.
    """

    class Meta:
        model = Address
        fields = (
            "id",
            "address_type",
            "address_line",
            "latitude",
            "longitude",
            "is_default",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError("Latitude must be between -90 and 90.")
        return value

    def validate_longitude(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError("Longitude must be between -180 and 180.")
        return value
