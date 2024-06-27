from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    """
    Модель курса.

    Attributes:
        name (CharField): Название курса.
        course_preview (ImageField): Превью (картинка) курса.
        description (TextField): Описание курса.
    """
    name = models.CharField(max_length=100, verbose_name='Название курса', help_text='Укажите название курса')
    course_preview = models.ImageField(upload_to='materials/photo', verbose_name='Фото',
                                       help_text='Загрузите фото курса', **NULLABLE)
    description = models.TextField(**NULLABLE, verbose_name='Описание курса', help_text='Укажите описание курса')

    owner = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Владелец',
                              help_text='Укажите владельца курса')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """
    Модель урока.

    Attributes:
        name (CharField): Название урока.
        course (ForeignKey): Ссылка на курс, к которому относится урок.
        lesson_preview (ImageField): Превью (картинка) урока.
        link_to_video (URLField): Ссылка на видео урока.
    """
    name = models.CharField(max_length=100, verbose_name='Урок', help_text='Укажите название урока')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name='Курс', help_text='Выберите курс',
                               **NULLABLE)
    lesson_preview = models.ImageField(upload_to='materials/photo', verbose_name='Фото',
                                       help_text='Загрузите фото урока', **NULLABLE)
    link_to_video = models.URLField(verbose_name='Ссылка на видео', help_text='Укажите ссылку на видео урока',
                                    **NULLABLE)
    owner = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Владелец',
                              help_text='Укажите владельца урока')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.name
