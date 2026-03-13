from rest_framework.pagination import PageNumberPagination


class PaginationHabit(PageNumberPagination):
    page_size = 5
    page_size_query_param = (
        "page_size"  # Параметр запроса для указания количества элементов на странице
    )
    max_page_size = 10
