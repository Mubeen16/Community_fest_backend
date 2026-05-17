from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """Ensure all API errors return consistent JSON format."""
    response = exception_handler(exc, context)
    if response is not None and isinstance(response.data, list):
        response.data = {"detail": response.data[0]}
    return response
