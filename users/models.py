from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    """
    Модель пользователя, расширяющая стандартную модель AbstractUser.
    Авторизация по email вместо username.

    Attributes:
        email (EmailField): Почта пользователя, используется для авторизации.
        phone (CharField): Телефон пользователя.
        city (CharField): Город пользователя.
        avatar (ImageField): Аватар пользователя.
    """
    username = None
    email = models.EmailField(unique=True, verbose_name="Почта", help_text="Укажите почту")

    phone = models.CharField(max_length=35, blank=True, null=True, verbose_name="Телефон", help_text="Укажите телефон")
    city = models.CharField(max_length=50, blank=True, null=True, verbose_name="Город", help_text="Укажите Ваш город")
    avatar = models.ImageField(upload_to="users/avatars", blank=True, null=True, verbose_name="Аватар",
                               help_text="Загрузите фото")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    """
    Модель для хранения информации о платежах пользователей.
    """
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    payment_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name="Оплаченный курс")
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, null=True, blank=True,
                                    verbose_name="Оплаченный урок")
    amount = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name="Способ оплаты")

    stripe_session_id = models.CharField(max_length=255, blank=True, null=True,
                                         verbose_name="Идентификатор сессии Stripe")
    stripe_payment_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Ссылка на оплату в Stripe")

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f'{self.user} - {self.amount} - {self.payment_method}'
