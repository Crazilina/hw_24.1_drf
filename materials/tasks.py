from celery import shared_task
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
from materials.models import Subscription
from materials.models import Lesson


@shared_task
def send_lesson_update_email(lesson_id):
    """Отправляет email-уведомление всем подписчикам курса о его обновлении."""
    lesson = Lesson.objects.get(id=lesson_id)  # Получаем обновленный урок по его идентификатору
    course = lesson.course  # Получаем курс, к которому относится урок
    subscribers = Subscription.objects.filter(course=course)  # Получаем всех подписчиков курса
    recipient_list = []
    for sub in subscribers:
        recipient_list.append(sub.user.email)  # Заполняем список email-адресов подписчиков

    if recipient_list:
        subject = f'Урок "{lesson.name}" обновлен в курсе {course.name}'
        message = f'Урок "{lesson.name}" в курсе {course.name} был обновлен. Проверьте новые материалы!'
        from_email = EMAIL_HOST_USER

        send_mail(subject, message, from_email, recipient_list)
