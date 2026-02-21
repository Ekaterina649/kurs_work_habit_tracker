from django.db import models
from django.core.exceptions import ValidationError

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

    def __str__(self):
        type_habit = "Приятная" if self.is_pleasant else "Полезная"
        return f"{type_habit}: {self.action} в {self.time} ({self.place})"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
