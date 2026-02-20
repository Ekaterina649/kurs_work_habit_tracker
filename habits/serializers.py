from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("owner",)

    def validate(self, data):

        related = data.get("related_habit")
        reward = data.get("reward")
        is_pleasant = data.get("is_pleasant")

        if related and reward:
            raise serializers.ValidationError(
                "Нельзя одновременно указывать связанную привычку и вознаграждение."
            )

        if is_pleasant and (related or reward):
            raise serializers.ValidationError(
                "У приятной привычки не может быть награды."
            )

        return data