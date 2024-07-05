from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer, URLField

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_youtube_link


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
    link_to_video = URLField(validators=[validate_youtube_link])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    """
       Сериализатор для модели Course, который включает количество уроков и информацию по всем урокам курса.

       Attributes:
           lesson_count (SerializerMethodField): Количество уроков в курсе.
           lessons (LessonSerializer): Информация по всем урокам курса.
       """
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    is_subscribed = SerializerMethodField()

    def get_lesson_count(self, course):
        """
        Метод для подсчета количества уроков в курсе.
        """
        return Lesson.objects.filter(course=course).count()

    def get_is_subscribed(self, course):
        """
        Метод для определения, подписан ли текущий пользователь на курс.
        """
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=course).exists()
        return False

    class Meta:
        model = Course
        fields = ("name", "course_preview", "description", "lesson_count", "lessons", "is_subscribed")


class SubscriptionSerializer(ModelSerializer):
    """
    Сериализатор для модели Subscription.

    Attributes:
        user (User): Пользователь, который подписан на курс.
        course (Course): Курс, на который пользователь подписан.
    """

    class Meta:
        model = Subscription
        fields = ['user', 'course']
