from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from multilibrary.helpers import generate_formatted_response


class FilePageNumberPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        response_status = status.HTTP_200_OK
        response_data = generate_formatted_response(status=True, payload={'files': data})
        response_data['next'] = self.get_next_link()
        response_data['prev'] = self.get_previous_link()
        response_data['count'] = self.page.paginator.count
        return Response(response_data, status=response_status)