from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny


class RegisterView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = RegisterSerializer
