from celery import shared_task

from habits.models import Habit
from habits.services import telegram_sendMessage


@shared_task
def send_habit_reminders():
    habits = Habit.objects.all()
    print("Запуск задачи, проверка привычек:", habits.count())
    for habit in habits:
        print("Проверяем привычку:", habit)
        if habit.is_due_now(minutes_interval=5):
            print("Привычка должна сработать:", habit.action)
            chat_id = habit.owner.telegram_chat_id
            if chat_id:
                habit_type = "приятную" if habit.is_pleasant else "полезную"
                telegram_sendMessage(
                    f"Не забудьте выполнить {habit_type} привычку: {habit.action} ({habit.time})",
                    chat_id,
                )
            else:
                print("Нет chat_id для пользователя:", habit.owner)
