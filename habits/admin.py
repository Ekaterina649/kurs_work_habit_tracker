from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "owner",
        "action",
        "place",
        "time",
        "is_pleasant",
        "is_public",
    )
