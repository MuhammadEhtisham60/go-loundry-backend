from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.authentication.serializers.otp_serializer import (
    OtpTriggerSerializer,
    OtpVerifySerializer,
)
from apps.authentication.serializers.user_serializer import UserSerializer
from apps.authentication.services.auth_service import AuthService
from common.responses.standard import StandardResponse


class OtpTriggerView(APIView):
    """
    API View to request/trigger an OTP.
    """

    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = OtpTriggerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        phone = serializer.validated_data.get("phone")

        AuthService.trigger_otp(email=email, phone=phone)

        return StandardResponse(
            data=None,
            message="Verification OTP sent successfully.",
            status=status.HTTP_200_OK,
        )


class OtpVerifyView(APIView):
    """
    API View to verify OTP and issue JWT login tokens.
    """

    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = OtpVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        phone = serializer.validated_data.get("phone")
        otp_code = serializer.validated_data.get("otp_code")

        user = AuthService.verify_otp(
            otp_code=otp_code, email=email, phone=phone
        )
        tokens = AuthService.generate_tokens(user)
        user_data = UserSerializer(user).data

        payload = {
            "tokens": tokens,
            "user": user_data,
        }

        return StandardResponse(
            data=payload,
            message="OTP verified and login successful.",
            status=status.HTTP_200_OK,
        )
