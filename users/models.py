from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Номер телефона"
    )

    telegram_chat_id = models.BigIntegerField(
        null=True,
        blank=True,
        unique=True,
        verbose_name="Telegram Chat ID"
    )

    telegram_username = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Telegram username"
    )


    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
