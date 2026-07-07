from typing import Any, Optional
from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from common.responses.standard import StandardResponse


def custom_exception_handler(exc: Exception, context: Any) -> Optional[Response]:
    """
    Custom exception handler for Django REST Framework.
    Wraps standard API exceptions and validation errors into the StandardResponse format.
    """
    response = exception_handler(exc, context)

    if response is not None:
        data = response.data
        message = "An error occurred"
        errors = None

        if isinstance(exc, ValidationError):
            message = "Validation failed"
            errors = data
        else:
            if isinstance(data, dict):
                if "detail" in data:
                    message = str(data["detail"])
                else:
                    errors = data
            elif isinstance(data, list):
                if len(data) > 0:
                    message = str(data[0])
            else:
                message = str(data)

        # Wrap in StandardResponse
        return StandardResponse(
            data=None,
            message=message,
            status=response.status_code,
            success=False,
            errors=errors
        )

    return None
