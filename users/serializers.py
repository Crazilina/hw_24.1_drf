from rest_framework.serializers import ModelSerializer, CharField

from users.models import Payment, User


class PaymentSerializer(ModelSerializer):
    """ Сериализатор для модели Payment. """

    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['user', 'stripe_session_id', 'stripe_payment_url']


class UserSerializer(ModelSerializer):
    """
    Сериализатор для модели User для стандартных CRUD операций.
    """
    password = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'password']


class UserProfileSerializer(ModelSerializer):
    """
    Сериализатор для модели User с включенной историей платежей.
    """
    payments = PaymentSerializer(many=True, read_only=True, source='payment_set')

    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar', 'payments']
