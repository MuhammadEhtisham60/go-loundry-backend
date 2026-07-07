from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.authentication.serializers.social_serializer import SocialLoginSerializer
from apps.authentication.serializers.user_serializer import UserSerializer
from apps.authentication.services.auth_service import AuthService
from common.responses.standard import StandardResponse


class SocialLoginView(APIView):
    """
    API View to simulate Google or Facebook social sign-in/sign-up.
    """

    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        serializer = SocialLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = AuthService.social_login(serializer.validated_data)
        tokens = AuthService.generate_tokens(user)
        user_data = UserSerializer(user).data

        payload = {
            "tokens": tokens,
            "user": user_data,
        }

        return StandardResponse(
            data=payload,
            message="Social login successful.",
            status=status.HTTP_200_OK,
        )
