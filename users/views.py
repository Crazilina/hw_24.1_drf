from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from users.models import Payment, User
from users.serializers import PaymentSerializer, UserProfileSerializer, UserSerializer

from rest_framework.permissions import IsAuthenticated, AllowAny


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
        """
        Возвращает соответствующий сериализатор в зависимости от действия.

        - Для действия 'retrieve' возвращает UserProfileSerializer для включения истории платежей.
        - Для всех остальных действий возвращает UserSerializer.
        """
        if self.action == "retrieve":
            return UserProfileSerializer
        return UserSerializer

    def get_permissions(self):
        """
        Возвращает соответствующие разрешения в зависимости от действия.

        - Для действия 'create' возвращает AllowAny для разрешения создания пользователя без аутентификации.
        - Для всех остальных действий возвращает IsAuthenticated для защиты действий аутентификацией.
        """
        if self.action in ['create']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """
        Переопределяет метод сохранения для установки пароля пользователя и активации учетной записи.

        - Устанавливает пароль, используя set_password для сохранения пароля в зашифрованном виде.
        - Устанавливает is_active в True для активации учетной записи.
        """
        user = serializer.save(is_active=True)
        user.set_password(serializer.validated_data['password'])
        user.save()

