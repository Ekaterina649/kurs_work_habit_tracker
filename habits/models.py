from django.db import models

from users.models import User


class Habit(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Владелец"
    )

    place = models.CharField(max_length=255,verbose_name="Место",help_text="Укажите место")
    time = models.TimeField(verbose_name="Время",help_text="Укажите время")
    action = models.CharField(max_length=255,verbose_name="Действие",help_text="Укажите действие")
    is_pleasant = models.BooleanField(default=False,verbose_name="Приятная привычка")

    related_habit = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='related_to',
        verbose_name="Связанная привычка"
    )

    frequency = models.PositiveIntegerField(default=1,verbose_name="Частота повторения",help_text="Периодичность в днях")  # раз в N дней
    reward = models.CharField(max_length=255, blank=True, null=True,verbose_name="Вознаграждение",help_text="Укажите вознаграждение")
    execution_time = models.PositiveIntegerField(verbose_name="Время выполнения",help_text="Укажите время выполнения")  # в секундах
    is_public = models.BooleanField(default=False,verbose_name="Публичность")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} {self.time} {self.place}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
