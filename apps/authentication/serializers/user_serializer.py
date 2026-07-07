from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying basic User model details safely.
    """

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone",
            "full_name",
            "role",
            "profile_photo",
            "is_blocked",
            "created_at",
            "updated_at",
        )

        read_only_fields = ("id", "created_at", "updated_at")

