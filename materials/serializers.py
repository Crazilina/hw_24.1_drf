from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(ModelSerializer):
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

    def get_lesson_count(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ("name", "course_preview", "description", "lesson_count", "lessons")
