from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'limit'
    max_page_size = 100

    def get_paginated_response(self, data):
        if 'limit' in self.request.query_params:
            self.page_size = self.request.query_params['limit']
        return super().get_paginated_response(data)
