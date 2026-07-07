from typing import Dict, Any
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.reviews.models import Review
from apps.orders.models import Order, OrderStatus

User = get_user_model()


class ReviewService:
    """
    Service layer containing operations for creating customer reviews.
    """

    @staticmethod
    def create_review(user: User, validated_data: Dict[str, Any]) -> Review:
        """
        Creates a review after verifying ownership and status checks.
        """
        order_id = validated_data["order_id"]
        rating = validated_data["rating"]
        remarks = validated_data.get("remarks", "")

        order = get_object_or_404(Order, id=order_id)

        if order.user != user:
            raise serializers.ValidationError("You can only rate your own orders.")

        if order.status != OrderStatus.DELIVERED:
            raise serializers.ValidationError(
                "Reviews are only allowed for delivered orders."
            )

        if hasattr(order, "review"):
            raise serializers.ValidationError(
                "You have already reviewed this order."
            )

        with transaction.atomic():
            review = Review.objects.create(
                user=user, order=order, rating=rating, remarks=remarks
            )
            return review
