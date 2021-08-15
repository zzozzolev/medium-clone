from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "page_size"
    # default page size
    page_size = 10
    max_page_size = 50
