# from rest_framework.viewsets import ...
from django.core.exceptions import ValidationError
from django.http import Http404
from django.utils.translation import gettext as _
from drf_multiple_model.views import ObjectMultipleModelAPIView
from rest_framework import serializers
from rest_framework.exceptions import ErrorDetail
from rest_framework.generics import RetrieveAPIView, DestroyAPIView, ListAPIView, UpdateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


from .models import Proposal, City, Category, CityArea
from .serializers import ProposalSerializer, CitySerializer, CategorySerializer


class ProposalAPIView(ListAPIView):
    """
    ListAPIView extended by GenaricAPIView, GenericAPIView has pagination, queryset, serializer_class etc.
    Use get(), post(), etc instead create(), retrive(), etc
    """
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer


class ProposalProposalAPIViewDetails(RetrieveAPIView, DestroyAPIView):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer

    def patch(self, request, pk):
        instance = self.get_object()

        field_errors = {}

        # Convert UUID to foreign key data object
        # TODO: refactor it
        if 'category' in request.data:
            try:
                categiry = Category.objects.get(
                    pk=request.data.get('category'))
                instance.category = categiry
            except:
                field_errors['category'] = [ErrorDetail(_(
                    "This category doesn't exists."), code="wrong_category")]

        if 'city' in request.data:
            # city
            # TODO: depending on city_area
            try:
                city = City.objects.get(
                    pk=request.data.get('city'))
                instance.city = city
            except:
                field_errors['city'] = [ErrorDetail(_(
                    "This city doesn't exists."), code="wrong_city")]

        if 'city_area' in request.data:
            # TODO: depending on city
            try:
                city_area = City.objects.get(
                    pk=request.data.get('city_area'))
                instance.city_area = city_area
            except:
                field_errors['city_area'] = [ErrorDetail(_(
                    "This city area doesn't exists."), code="wrong_city_area")]

        serializer = self.get_serializer(
            instance, data=request.data, partial=True)

        has_errors = serializer.is_valid() is False or len(field_errors.keys())

        if has_errors:
            field_errors.update(serializer.errors)
            raise serializers.ValidationError(field_errors)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        serializer.save()
        return Response(serializer.data)


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
