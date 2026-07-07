from rest_framework import serializers
from apps.reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer representing customer reviews.
    """

    class Meta:
        model = Review
        fields = ("id", "user", "order", "rating", "remarks", "created_at")
        read_only_fields = ("id", "user", "created_at")


class ReviewCreateSerializer(serializers.Serializer):
    """
    Validator for customer review creation inputs.
    """

    order_id = serializers.UUIDField(required=True)
    rating = serializers.IntegerField(required=True, min_value=1, max_value=5)
    remarks = serializers.CharField(required=False, allow_blank=True, default="")
