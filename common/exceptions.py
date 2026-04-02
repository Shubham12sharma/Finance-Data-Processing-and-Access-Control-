from rest_framework.views import exception_handler
from rest_framework.response import Response
from .responses import api_error


def custom_exception_handler(exc, context):
    """Custom exception handler for consistent error format"""
    response = exception_handler(exc, context)

    if response is not None:
        # Convert default DRF errors to our format
        if isinstance(response.data, dict):
            errors = response.data
        else:
            errors = {"detail": response.data}

        return api_error(
            message="Validation error" if response.status_code == 400 else "An error occurred",
            errors=errors,
            status=response.status_code
        )

    return response