from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import PaymentViewSet, UserViewSet, PaymentCreateAPIView

from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = SimpleRouter()

router.register(r'', UserViewSet)
router.register(r'payments', PaymentViewSet)

app_name = UsersConfig.name

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('payments/create/', PaymentCreateAPIView.as_view(), name='payments-create'),
] + router.urls
