from rest_framework.pagination import PageNumberPagination

# At the moment, this is not used
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'