from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.authentication.serializers.password_reset_serializer import (
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
)
from apps.authentication.services.auth_service import AuthService
from common.responses.standard import StandardResponse


class ForgotPasswordView(APIView):
    """
    API View to request a password reset code.
    """

    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        phone = serializer.validated_data.get("phone")

        AuthService.forgot_password(email=email, phone=phone)

        return StandardResponse(
            data=None,
            message="Password reset verification code sent.",
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    """
    API View to submit a new password using a verification code.
    """

    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        AuthService.reset_password(serializer.validated_data)

        return StandardResponse(
            data=None,
            message="Password has been reset successfully.",
            status=status.HTTP_200_OK,
        )
