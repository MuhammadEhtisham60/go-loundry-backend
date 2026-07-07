from typing import Any, Optional
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class StandardResponse(Response):
    """
    Standard HTTP Response formatter for Django REST Framework.
    Ensures all successful and error responses follow a consistent envelope structure:
    {
        "success": bool,
        "data": dict or list or null,
        "message": str or null,
        "errors": dict or null
    }
    """

    def __init__(
        self,
        data: Any = None,
        message: Optional[str] = None,
        status: int = HTTP_200_OK,
        success: bool = True,
        errors: Optional[Any] = None,
        **kwargs: Any
    ) -> None:
        formatted_data = {
            "success": success,
            "data": data,
            "message": message,
            "errors": errors,
        }
        super().__init__(data=formatted_data, status=status, **kwargs)
