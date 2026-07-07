from django.contrib.auth import authenticate
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    """
    Serializer validating login credentials.
    Supports email + password or phone + password.
    """

    email = serializers.EmailField(required=False, allow_null=True, default=None)
    phone = serializers.CharField(required=False, allow_null=True, default=None)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        email = data.get("email")
        phone = data.get("phone")
        password = data.get("password")

        if not email and not phone:
            raise serializers.ValidationError(
                "Either email or phone number must be provided."
            )

        # Authenticate via custom backend (using email or phone as username)
        username = email or phone
        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email/phone or password.")

        if user.is_blocked:
            raise serializers.ValidationError("Your account has been blocked.")

        if not user.is_active:
            raise serializers.ValidationError("Your account is deactivated.")

        data["user"] = user
        return data
