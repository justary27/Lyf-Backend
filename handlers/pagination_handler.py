from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.pagination import PageNumberPagination


class LyfPaginator(PageNumberPagination):

    page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'per_page'
    max_page_size = 100
    
    def get_paginated_response(self, queryset, request, data: dict):
        self.paginate_queryset(queryset, request)

        data["content"]["links"] = {
            'next': self.get_next_link(),
            'previous': self.get_previous_link()
        }

        data["content"]["count"] = self.page.paginator.count
        
        return Response(data, HTTP_200_OK)


lyf_paginator = LyfPaginator()
