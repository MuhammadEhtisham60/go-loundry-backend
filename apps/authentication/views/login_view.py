from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.authentication.serializers.login_serializer import LoginSerializer
from apps.authentication.serializers.user_serializer import UserSerializer
from apps.authentication.services.auth_service import AuthService
from common.responses.standard import StandardResponse


class LoginView(APIView):
    """
    API view for user login.
    Authenticates user credentials and returns JWT access and refresh tokens.
    """

    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        """
        Validate request data, authenticate user, and issue access & refresh tokens.
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        tokens = AuthService.generate_tokens(user)
        user_data = UserSerializer(user).data

        payload = {
            "tokens": tokens,
            "user": user_data,
        }

        return StandardResponse(
            data=payload,
            message="Login successful.",
            status=status.HTTP_200_OK,
        )
