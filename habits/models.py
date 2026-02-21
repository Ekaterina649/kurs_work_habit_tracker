from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime

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

    start_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Дата начала",
        help_text="С какого дня начинает действовать привычка. Если не указана — с даты создания."
    )

    def clean(self):
        errors = {}

        if self.related_habit and self.reward:
            errors['__all__'] = "Нельзя одновременно указывать связанную привычку и вознаграждение."

        if self.execution_time > 120:
            errors['execution_time'] = "Время выполнения не должно превышать 120 секунд."

        if self.is_pleasant:
            if self.reward or self.related_habit:
                errors['__all__'] = "У приятной привычки не может быть вознаграждения или связанной привычки."

        if self.frequency > 7:
            errors['frequency'] = "Нельзя выполнять привычку реже одного раза в 7 дней."

        if self.related_habit:
            if not self.related_habit.is_pleasant:
                errors['related_habit'] = "Связанной может быть только приятная привычка."
            if self.related_habit.owner != self.owner:
                errors['related_habit'] = "Можно привязывать только свои приятные привычки."

        if errors:
            raise ValidationError(errors)

        super().clean()

    def is_due_now(self, minutes_interval: int = 5) -> bool:
        """
        Проверяет, нужно ли сейчас выполнить привычку.
        Учитывается дата и время с интервалом +/- minutes_interval минут.
        """
        now = timezone.localtime()
        today = now.date()

        # Проверка старта привычки
        if self.start_date and today < self.start_date:
            return False

        # Проверка по дню выполнения
        days_since_start = (today - (self.start_date or self.created_at.date())).days
        if days_since_start < 0 or self.frequency == 0:
            return False

        if days_since_start % self.frequency != 0:
            return False

        # Проверка времени привычки ±interval минут
        habit_datetime = timezone.make_aware(
            datetime.combine(today, self.time)
        )
        delta_seconds = (habit_datetime - now).total_seconds()
        return -minutes_interval * 60 <= delta_seconds <= minutes_interval * 60

    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = timezone.now().date()
        super().save(*args, **kwargs)

    def __str__(self):
        type_habit = "Приятная" if self.is_pleasant else "Полезная"
        return f"{type_habit}: {self.action} в {self.time} ({self.place})"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
