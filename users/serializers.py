from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class PaymentSerializer(ModelSerializer):
    """
    Сериализатор для модели Payment.

    Attributes:
        model (Model): Модель Payment.
        fields (str): Поля для сериализации.
    """
    class Meta:
        model = Payment
        fields = "__all__"


class UserProfileSerializer(ModelSerializer):
    """
    Сериализатор для модели User с включенной историей платежей.
    """
    payments = PaymentSerializer(many=True, read_only=True, source='payment_set')

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'payments']
