from typing import Any
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.request import Request
from rest_framework.response import Response
from common.responses.standard import StandardResponse


class CustomTokenRefreshView(TokenRefreshView):
    """
    Subclass of SimpleJWT's TokenRefreshView to format the response
    using the standard API response structure.
    """

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        response = super().post(request, *args, **kwargs)
        return StandardResponse(
            data=response.data,
            message="Token refreshed successfully.",
            status=response.status_code,
        )
