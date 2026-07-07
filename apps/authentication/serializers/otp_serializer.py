from rest_framework import serializers


class OtpTriggerSerializer(serializers.Serializer):
    """
    Serializer to trigger OTP generation.
    Supports email or phone.
    """

    email = serializers.EmailField(required=False, allow_null=True, default=None)
    phone = serializers.CharField(required=False, allow_null=True, default=None)

    def validate(self, data):
        if not data.get("email") and not data.get("phone"):
            raise serializers.ValidationError(
                "Either email or phone is required to trigger OTP."
            )
        return data


class OtpVerifySerializer(serializers.Serializer):
    """
    Serializer to verify OTP and log in.
    """

    email = serializers.EmailField(required=False, allow_null=True, default=None)
    phone = serializers.CharField(required=False, allow_null=True, default=None)
    otp_code = serializers.CharField(max_length=6, required=True)

    def validate(self, data):
        if not data.get("email") and not data.get("phone"):
            raise serializers.ValidationError(
                "Either email or phone is required to verify OTP."
            )
        return data
