from rest_framework.views import Response, exception_handler

from handlers.response_handler import ResponseData

def api_exception_handler(exception: Exception, context: dict) -> Response:
    """Lyf's API exception handler."""

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exception, context)
    
    msg = {
        "message": response.data["detail"]
    }
    
    error_payload = ResponseData(
        response.status_code, msg
    ).get_data()
     
    return Response(error_payload, status=response.status_code)
