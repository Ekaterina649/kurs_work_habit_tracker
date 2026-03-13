from rest_framework import generics
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import UserSerializer


class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
