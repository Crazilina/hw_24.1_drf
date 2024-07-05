from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """
    Класс для настройки пагинации.
    """
    page_size = 3  # Количество элементов на странице
    page_size_query_param = 'page_size'  # Параметр для изменения количества элементов на странице
    max_page_size = 10  # Максимальное количество элементов на странице
