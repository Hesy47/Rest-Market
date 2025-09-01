from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.exceptions import AuthenticationFailed as DRFAuthenticationFailed


def normalize_errors_output(data):
    """My custom error handler for DRF ValidationError"""

    if isinstance(data, list):
        return {"non_field_errors": [str(v) for v in data]}

    if isinstance(data, dict):
        normalized = {}

        for key, value in data.items():
            if isinstance(value, (list, tuple)):
                normalized[key] = [str(v) for v in value]
            else:
                normalized[key] = [str(value)]
        return normalized

    return {"non_field_errors": [str(data)]}


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, DRFValidationError):
        errors = normalize_errors_output(response.data if response else exc.detail)
        return Response(
            {
                "status": "error",
                "message": "Validation failed",
                "errors": errors,
            },
            status=response.status_code if response else status.HTTP_400_BAD_REQUEST,
        )

    if isinstance(exc, DRFAuthenticationFailed):
        errors = {"authentication": [str(exc.detail)]}
        return Response(
            {
                "status": "error",
                "message": "Authentication failed",
                "errors": errors,
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    return response
