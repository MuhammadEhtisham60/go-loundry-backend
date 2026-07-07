from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    """
    Serializer to validate user registration inputs.
    Supports signing up with email/password, phone/password, or both.
    """

    email = serializers.EmailField(required=False, allow_null=True, default=None)
    phone = serializers.CharField(
        max_length=20, required=False, allow_null=True, default=None
    )
    password = serializers.CharField(
        write_only=True, required=False, allow_null=True, default=None
    )
    password_confirm = serializers.CharField(
        write_only=True, required=False, allow_null=True, default=None
    )
    full_name = serializers.CharField(max_length=255, required=False, allow_blank=True, default="")

    def validate(self, data):
        email = data.get("email")
        phone = data.get("phone")
        password = data.get("password")
        password_confirm = data.get("password_confirm")

        if not email and not phone:
            raise serializers.ValidationError(
                "Either email or phone number must be provided for registration."
            )

        if email:
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    {"email": "A user with this email address already exists."}
                )

        if phone:
            if User.objects.filter(phone=phone).exists():
                raise serializers.ValidationError(
                    {"phone": "A user with this phone number already exists."}
                )

        # Validate password if provided
        if password or password_confirm:
            if password != password_confirm:
                raise serializers.ValidationError(
                    {"password_confirm": "Passwords do not match."}
                )
            if password:
                validate_password(password)

        return data
