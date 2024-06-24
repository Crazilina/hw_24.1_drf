from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserProfileSerializer


class PaymentViewSet(ModelViewSet):
    """
    Viewset для выполнения CRUD операций над моделью Payment, с добавлением фильтрации и сортировки.

    Attributes:
        queryset (QuerySet): Запрос для получения всех платежей.
        filter_backends (tuple): Кортеж фильтров для использования в ViewSet.
        filterset_fields (list): Поля для фильтрации.
        ordering_fields (list): Поля для сортировки.
        search_fields (list): Поля для поиска.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']
    search_fields = ['user__email']


class UserViewSet(ModelViewSet):
    """
    Viewset для выполнения CRUD операций над моделью User с включенной историей платежей.
    """
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserProfileSerializer
        return UserProfileSerializer
