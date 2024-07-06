from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Lesson, Course, Subscription
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        """
        Метод для подготовки тестовых данных.
        """
        self.user = User.objects.create(email="test@testov.com")

        self.course = Course.objects.create(
            name='Тестовый курс',
            description='Тестовое описание',
            owner=self.user
        )

        self.lesson = Lesson.objects.create(
            name='Тестовый урок',
            course=self.course,
            link_to_video='https://youtube.com/testvideo',
            owner=self.user
        )

        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        """
        Тест получения информации о курсе.
        """
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), self.course.name
        )
        self.assertEqual(
            data.get("is_subscribed"), False
        )

    def test_course_create(self):
        """
        Тест создания курса.
        """
        url = reverse("materials:course-list")
        data = {
            "name": "Новый курс",
            "description": "Новое описание"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Course.objects.all().count(), 2
        )

    def test_course_update(self):
        """
        Тест обновления курса.
        """
        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {
            "name": "Обновленный курс"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("name"), "Обновленный курс"
        )

    def test_course_delete(self):
        """
        Тест удаления курса.
        """
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Course.objects.all().count(), 0
        )

    def test_course_list(self):
        """
        Тест списка курсов.
        """
        url = reverse("materials:course-list")
        response = self.client.get(url)
        data = response.json()
        expected_data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "name": "Тестовый курс",
                    "course_preview": None,
                    "description": "Тестовое описание",
                    "owner": self.user.pk,
                    "lesson_count": 1,
                    "lessons": [
                        {
                            "id": self.lesson.pk,
                            "name": "Тестовый урок",
                            "course": self.course.pk,
                            "lesson_preview": None,
                            "link_to_video": "https://youtube.com/testvideo",
                            "owner": self.user.pk
                        }
                    ],
                    "is_subscribed": False
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, expected_data)


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='user1@example.com')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            name="Тестовый курс",
            description="Тестовое описание",
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            name="Тестовый урок",
            course=self.course,
            link_to_video="https://youtube.com/testvideo",
            owner=self.user
        )

    def test_lesson_retrieve(self):
        """
        Тест получения информации об уроке.
        """
        url = reverse("materials:lessons-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.lesson.name)

    def test_lesson_create(self):
        """
        Тест создания нового урока.
        """
        url = reverse("materials:lessons-create")
        data = {
            "name": "Новый урок",
            "course": self.course.pk,
            "link_to_video": "https://youtube.com/newvideo",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        """
        Тест обновления информации об уроке.
        """
        url = reverse("materials:lessons-update", args=(self.lesson.pk,))
        data = {
            "name": "Обновленный урок"
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Обновленный урок")

    def test_lesson_delete(self):
        """
        Тест удаления урока.
        """
        url = reverse("materials:lessons-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """
        Тест списка уроков.
        """
        url = reverse("materials:lessons-list")
        response = self.client.get(url)
        data = response.json()
        expected_data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": "Тестовый урок",
                    "course": self.course.pk,
                    "lesson_preview": None,
                    "link_to_video": "https://youtube.com/testvideo",
                    "owner": self.user.pk
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, expected_data)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='user1@example.com')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            name="Тестовый курс",
            description="Тестовое описание",
            owner=self.user
        )

    def test_subscribe(self):
        """
        Тест добавления подписки.
        """
        url = reverse("materials:subscribe")
        data = {
            "course_id": self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка добавлена")
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe(self):
        """
        Тест удаления подписки.
        """
        Subscription.objects.create(user=self.user, course=self.course)
        url = reverse("materials:subscribe")
        data = {
            "course_id": self.course.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Подписка удалена")
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
