from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.authentication.serializers.user_serializer import UserSerializer
from common.responses.standard import StandardResponse


class ProfileView(APIView):
    """
    API view for getting and updating the authenticated user's profile.
    Requires JWT authentication.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request: Request) -> Response:
        """
        Return the profile details of the current logged-in user.
        """
        user_data = UserSerializer(request.user).data
        return StandardResponse(
            data=user_data,
            message="Profile retrieved successfully.",
            status=status.HTTP_200_OK,
        )

    def put(self, request: Request) -> Response:
        """
        Update the current user's profile details.
        """
        user = request.user
        
        # Partially update user profile fields
        user.full_name = request.data.get("full_name", user.full_name)
        user.profile_photo = request.data.get("profile_photo", user.profile_photo)
        user.save()

        user_data = UserSerializer(user).data
        return StandardResponse(
            data=user_data,
            message="Profile updated successfully.",
            status=status.HTTP_200_OK,
        )
