from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class ForgotPasswordSerializer(serializers.Serializer):
    """
    Serializer for forgot-password requests.
    """

    email = serializers.EmailField(required=False, allow_null=True, default=None)
    phone = serializers.CharField(required=False, allow_null=True, default=None)

    def validate(self, data):
        if not data.get("email") and not data.get("phone"):
            raise serializers.ValidationError(
                "Either email or phone is required to request a password reset."
            )
        return data


class ResetPasswordSerializer(serializers.Serializer):
    """
    Serializer to complete password resets with an OTP code.
    """

    email = serializers.EmailField(required=False, allow_null=True, default=None)
    phone = serializers.CharField(required=False, allow_null=True, default=None)
    otp_code = serializers.CharField(max_length=6, required=True)
    new_password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_confirm = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if not data.get("email") and not data.get("phone"):
            raise serializers.ValidationError(
                "Either email or phone is required."
            )

        if data["new_password"] != data["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": "Passwords do not match."}
            )

        return data
