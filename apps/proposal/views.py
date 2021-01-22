from drf_multiple_model.views import ObjectMultipleModelAPIView
from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny

from .models import Proposal, City, Category
from .serializers import ProposalSerializer, CitySerializer, CategorySerializer


class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer


class FiltersView(ObjectMultipleModelAPIView):
    permission_classes = [AllowAny]

    querylist = [
        {
            'queryset': Category.objects.all(),
            'serializer_class': CategorySerializer,
            'label': 'categories'
        },
        {
            'queryset': City.objects.all(),
            'serializer_class': CitySerializer,
            'label': "cities"
        },
    ]
