from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.pagination import PageNumberPagination

from constants.response_constants import SUCCESSFUL_RESPONSE
from enums.response_type import ResponseType


class LyfPaginator(PageNumberPagination):
    """
    The custom default paginator class for Lyf.
    """

    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'per_page'
    max_page_size = 100

    def __init__(self, request):
        self.request = request

    def get_paginated_response(self, data: list):
        result = self.paginate_queryset(data, self.request)

        extras = {
            "links": {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            "count": self.page.paginator.count
        }

        return Response(ResponseType.ok_request(
            SUCCESSFUL_RESPONSE, result, pagination_info=extras
        ).get_data(), HTTP_200_OK)
