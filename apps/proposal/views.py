from django.core.exceptions import ValidationError
from django.forms.models import model_to_dict
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from drf_multiple_model.views import ObjectMultipleModelAPIView
from rest_framework.exceptions import ErrorDetail, ParseError
from rest_framework.generics import DestroyAPIView, ListAPIView, UpdateAPIView, CreateAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED
from rest_framework.views import APIView


from ..profile.models import User
from .filters import ProposalFilter
from .models import Proposal, City, Category, CityArea
from .serializers import ProposalSerializer, ProposalDetailsSerializer, CitySerializer, CategorySerializer


class ProposalListAPIView(ListAPIView):
    permission_classes = [AllowAny]
    """
    Only for GET pagginated list
   
    ListAPIView extended by GenaricAPIView, GenericAPIView has pagination, queryset, serializer_class etc.
    Use get(), post(), etc instead create(), retrive(), etc
    """
    filterset_class = ProposalFilter
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer


class ProposalCreateUpdateAPIView(APIView):
    def post(self, request):
        request_serializer = ProposalDetailsSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        request_serializer.save()

        try:
            proposal_id = request_serializer.data.get('id')
            proposal = Proposal.objects.get(pk=proposal_id)
            response_serializer = ProposalSerializer(proposal)

            return Response(response_serializer.data, status=HTTP_201_CREATED)
        except:
            raise ParseError(_(f"{pk} is invalid proposal id."),
                             code='invalid_proposal_id')


class ProposalDetailsAPIView(APIView):
    def get(self, request, pk):
        try:
            proposal = Proposal.objects.get(pk=pk)
            serializer = ProposalSerializer(proposal)
        except:
            raise ParseError(_(f"{pk} is invalid proposal id."),
                             code='invalid_proposal_id')

        return Response(serializer.data)

    def delete(self, request, pk):
        try:
            Proposal.objects.get(pk=pk).delete()
        except:
            raise ParseError(_(f"{pk} is not found."),
                             code='proposal_not_found')

        return Response(status=HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        try:
            proposal = Proposal.objects.get(pk=pk)
        except:
            raise ParseError(_(f'{pk} is invalid proposal id.'),
                             code='invalid_proposal_id')

        request_serilaizer = ProposalDetailsSerializer(
            instance=proposal, data=request.data, partial=True)
        request_serilaizer.is_valid(raise_exception=True)
        request_serilaizer.save()

        responce_serializer = ProposalSerializer(proposal)

        return Response(responce_serializer.data, status=HTTP_201_CREATED)


class FiltersView(ObjectMultipleModelAPIView):
    permission_classes = [AllowAny]
    pagination_class = None
    querylist = [
        {
            'label': 'categories',
            'queryset': Category.objects.all(),
            'serializer_class': CategorySerializer,
        },
        {
            'label': 'cities',
            'queryset': City.objects.all(),
            'serializer_class': CitySerializer,
        },
    ]
