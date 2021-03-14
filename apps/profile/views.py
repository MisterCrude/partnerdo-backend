from django.shortcuts import render
from rest_framework.generics import RetrieveAPIView

from .serializers import UserSerializer
from .models import User


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
