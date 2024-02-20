from enum import Enum
from rest_framework import status
from handlers.response_handler import ResponseData
from constants.response_constants import INVALID_REQUEST_RESPONSE, \
    BAD_REQUEST_RESPONSE, DOES_NOT_EXIST_RESPONSE, UNAUTHORIZED_RESPONSE


class ResponseType(Enum):

    INVALID_REQUEST = ResponseData(
        status.HTTP_405_METHOD_NOT_ALLOWED, INVALID_REQUEST_RESPONSE
    )

    BAD_REQUEST = ResponseData(
        status.HTTP_400_BAD_REQUEST, BAD_REQUEST_RESPONSE
    )

    DOES_NOT_EXIST = ResponseData(
        status.HTTP_404_NOT_FOUND, DOES_NOT_EXIST_RESPONSE
    )

    UNAUTHORIZED_REQUEST = ResponseData(
        status.HTTP_403_FORBIDDEN, UNAUTHORIZED_RESPONSE
    )

    @staticmethod
    def ok_request(msg: str, data=None, **kwargs):
        content = {
            "message": msg,
        }

        if data is not None:
            content["data"] = data

        try:
            content.update(kwargs["pagination_info"])
        except KeyError:
            pass

        return ResponseData(
            status.HTTP_200_OK, content
        )
