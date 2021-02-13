from django.http import Http404
from drf_multiple_model.views import ObjectMultipleModelAPIView
from rest_framework import viewsets, generics, views, response, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import serializers
from django.utils.translation import gettext as _


from .models import Proposal, City, Category
from .serializers import ProposalSerializer, CitySerializer, CategorySerializer


class ProposalViewSet(viewsets.ModelViewSet):
    """
    ModelViewSet automaticaly implement
        + def list(self, request): GET
        + def create(self, request): POST
        + def retrieve(self, request, pk=None): GET
        + def update(self, request, pk=None): PUT
        + def partial_update(self, request, pk=None): PATCH
        + def destroy(self, request, pk=None): DELETE
    """
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
