from rest_framework.pagination import PageNumberPagination


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 60
    page_size_query_param = 'size'
    max_page_size = 100


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'size'
    max_page_size = 100


class MobileResultsSetPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'size'
    max_page_size = 24
