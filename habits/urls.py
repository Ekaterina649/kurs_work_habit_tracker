from django.urls import path, include
from rest_framework import routers
from .views import HabitViewSet

app_name = "habits"


router = routers.DefaultRouter()
router.register("", HabitViewSet, basename="habits")


urlpatterns = [
    path("", include(router.urls)),
]
