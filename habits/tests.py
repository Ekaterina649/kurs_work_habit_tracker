from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from users.models import User
from habits.models import Habit


class HabitModelValidationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpass123"
        )

    def test_cannot_have_both_reward_and_related_habit(self):
        pleasant = Habit.objects.create(
            owner=self.user,
            place="Дом",
            time="18:00:00",
            action="Читать книгу",
            is_pleasant=True,
            execution_time=60,
        )
        useful = Habit(
            owner=self.user,
            place="Кофейня",
            time="07:30:00",
            action="Выпить кофе",
            reward="Съесть круассан",
            related_habit=pleasant,
            execution_time=15,
        )
        with self.assertRaises(Exception):
            useful.full_clean()

    def test_pleasant_habit_cannot_have_reward(self):
        habit = Habit(
            owner=self.user,
            place="Парк",
            time="08:00:00",
            action="Прогулка",
            is_pleasant=True,
            reward="Послушать музыку",
            execution_time=45,
        )
        with self.assertRaises(Exception):
            habit.full_clean()

    def test_execution_time_more_than_120_seconds_not_allowed(self):
        habit = Habit(
            owner=self.user,
            place="Дом",
            time="20:00:00",
            action="Медитация",
            is_pleasant=True,
            execution_time=180,
        )
        with self.assertRaises(Exception):
            habit.full_clean()


class HabitAPITests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="apiuser", email="apiuser@example.com", password="apipass123"
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.url = "/habits/"

    def test_create_habit_success(self):
        payload = {
            "place": "Офис",
            "time": "09:15:00",
            "action": "Начать рабочий день с плана",
            "is_pleasant": False,
            "frequency": 1,
            "execution_time": 30,
            "is_public": False,
        }
        response = self.client.post(self.url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.first().owner, self.user)

    def test_list_only_own_habits(self):
        other_user = User.objects.create_user(
            username="other", email="other@example.com", password="pass123"
        )
        Habit.objects.create(
            owner=other_user,
            place="Test",
            time="12:00:00",
            action="Чужая привычка",
            execution_time=60,
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)
