from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.pagination import PaginationHabit
from habits.serializers import HabitSerializer, PublicHabitSerializer
from users.permissions import IsOwnerOrReadOnly


class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.none()
    serializer_class = HabitSerializer
    pagination_class = PaginationHabit
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]



    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == "public":
            return PublicHabitSerializer
        return HabitSerializer

    @action(detail=False, methods=["get"])
    def public(self, request):
        queryset = Habit.objects.filter(is_public=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


