from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView,
                                     DestroyAPIView)

from materials.models import Course, Lesson, Subscription
from materials.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer, SubscriptionSerializer

from rest_framework.permissions import IsAuthenticated

from users.permissions import IsModerator, IsOwner


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
        - Обычные пользователи могут управлять только своими курсами.
        """
        if self.action in ['create']:
            self.permission_classes = (~IsModerator,)
        elif self.action in ['destroy']:
            self.permission_classes = (IsOwner | ~IsModerator,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModerator | IsOwner,)
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Переопределяет метод создания объекта для привязки к авторизованному пользователю.
        """
        serializer.save(owner=self.request.user)


class LessonCreateAPIView(CreateAPIView):
    """
          Контроллер создания новых уроков.
          """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModerator, IsAuthenticated,)

    def perform_create(self, serializer):
        """
        Переопределяет метод создания объекта для привязки к авторизованному пользователю.
        """
        serializer.save(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    """
       Контроллер для получения списка уроков.
       """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRetrieveAPIView(RetrieveAPIView):
    """
        Контроллер для получения одного урока.
        """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner,)


class LessonUpdateAPIView(UpdateAPIView):
    """
            Контроллер для обновления одного урока.
            """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModerator | IsOwner,)


class LessonDestroyAPIView(DestroyAPIView):
    """
            Контроллер для удаления одного урока.
            """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModerator,)


class SubscriptionAPIView(APIView):
    """
    APIView для управления подписками на курсы.

    Methods:
        post: Добавляет или удаляет подписку пользователя на курс.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает запрос на добавление или удаление подписки пользователя на курс.
        """
        user = request.user
        course_id = request.data.get('course_id')
        course = get_object_or_404(Course, id=course_id)

        # Получаем объекты подписок по текущему пользователю и курса
        subscription = Subscription.objects.filter(user=user, course=course)
        if subscription.exists():
            # Если подписка у пользователя на этот курс есть - удаляем ее
            subscription.delete()
            message = 'Подписка удалена'
        else:
            # Если подписки у пользователя на этот курс нет - создаем ее
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'

        # Возвращаем ответ в API
        return Response({"message": message})
