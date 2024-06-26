from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView,
                                     DestroyAPIView)

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer

from rest_framework.permissions import IsAuthenticated

from users.permissions import IsModerator


class CourseViewSet(ModelViewSet):
    """
    Viewset для выполнения CRUD операций над моделью Course.
    """
    queryset = Course.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseDetailSerializer
        return CourseSerializer

    def get_permissions(self):
        """
        Устанавливает права доступа для различных действий.

        - Модераторы могут просматривать и редактировать курсы, но не могут их создавать или удалять.
        - Остальные пользователи должны быть аутентифицированы.
        """
        if self.action in ['create', 'destroy']:
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = [IsAuthenticated | IsModerator]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class LessonCreateAPIView(CreateAPIView):
    """
          Контроллер создания новых уроков.
          """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]


class LessonListAPIView(ListAPIView):
    """
       Контроллер для получения списка уроков.
       """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(RetrieveAPIView):
    """
        Контроллер для получения одного урока.
        """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated | IsModerator]


class LessonUpdateAPIView(UpdateAPIView):
    """
            Контроллер для обновления одного урока.
            """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated | IsModerator]


class LessonDestroyAPIView(DestroyAPIView):
    """
            Контроллер для удаления одного урока.
            """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]
