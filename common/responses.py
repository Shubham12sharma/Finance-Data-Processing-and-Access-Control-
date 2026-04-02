from rest_framework.response import Response


def api_success(data=None, message="Success", status=200):
    """Standard success response format"""
    response = {
        "success": True,
        "message": message,
    }
    if data is not None:
        response["data"] = data
    return Response(response, status=status)


def api_error(message="An error occurred", errors=None, status=400):
    """Standard error response format"""
    response = {
        "success": False,
        "message": message,
    }
    if errors:
        response["errors"] = errors
    return Response(response, status=status)