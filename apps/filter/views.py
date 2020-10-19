from drf_multiple_model.views import ObjectMultipleModelAPIView
from rest_framework import permissions

from .serializers import CitySerializer
from .models import City


class FilterAPIView(ObjectMultipleModelAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    querylist = (
        {'queryset': City.objects.all(),
         'serializer_class': CitySerializer,
         'label': 'cities'},

        # {'queryset': Service.objects.all(),
        #  'serializer_class': ServiceSerializer,
        #  'label': 'services'},
    )
