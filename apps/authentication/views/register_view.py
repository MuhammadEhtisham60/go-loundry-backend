from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.authentication.serializers.register_serializer import RegisterSerializer
from apps.authentication.serializers.user_serializer import UserSerializer
from apps.authentication.services.auth_service import AuthService
from common.responses.standard import StandardResponse


class RegisterView(APIView):
    """
    API view for registering a new user.
    Accessible by anyone.
    """

    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        """
        Validate credentials, register user, and return registration details.
        """
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = AuthService.register_user(serializer.validated_data)
        user_data = UserSerializer(user).data

        return StandardResponse(
            data=user_data,
            message="User registered successfully.",
            status=status.HTTP_201_CREATED,
        )
