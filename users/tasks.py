from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from users.models import User


@shared_task
def deactivate_inactive_users():
    """Деактивирует пользователей, которые не заходили более месяца."""
    one_month_ago = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=one_month_ago, is_active=True)

    for user in inactive_users:
        user.is_active = False
        user.save()
        print(f'User {user.email} has been deactivated.')
