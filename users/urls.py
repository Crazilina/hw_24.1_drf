from rest_framework.routers import SimpleRouter

from users.apps import UsersConfig
from users.views import PaymentViewSet, UserViewSet

router = SimpleRouter()
router.register(r'payments', PaymentViewSet)
router.register(r'users', UserViewSet)

app_name = UsersConfig.name

urlpatterns = [

] + router.urls
