from rest_framework import viewsets

from .serializers import UnitSerializer
from .models import Unit


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all().order_by('name')
    serializer_class = UnitSerializer
