from django.utils.translation import gettext as _
from rest_framework.exceptions import ParseError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT)
from rest_framework.views import APIView

from .filters import ProposalFilter
from .models import Category, City, Proposal
from .serializers import (FiltersSerializer, ProposalDetailsSerializer,
                          ProposalSerializer)

##
# Proposal
##


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


class ProposalCreateAPIView(APIView):
    def post(self, request):
        new_proposal_query_dict = request.data.copy()
        new_proposal_query_dict.__setitem__('author', request.user.id)

        request_serializer = ProposalDetailsSerializer(
            data=new_proposal_query_dict)
        request_serializer.is_valid(raise_exception=True)
        request_serializer.save()
        try:
            proposal_id = request_serializer.data.get('id')
            proposal = Proposal.objects.get(pk=proposal_id)
            response_serializer = ProposalSerializer(
                proposal, context={'request': request})

            return Response(response_serializer.data, status=HTTP_201_CREATED)
        except Exception:
            raise ParseError(_("Can't create new proposal."),
                             code='can_not_create_new_proposal')


class ProposalDetailsAPIView(APIView):
    def get(self, request, pk):
        try:
            proposal = Proposal.objects.get(pk=pk)
            serializer = ProposalSerializer(
                proposal, context={'request': request})
        except Exception:
            raise ParseError(_(f"{pk} is invalid proposal id."),
                             code='invalid_proposal_id')

        return Response(serializer.data, status=HTTP_200_OK)

    def delete(self, request, pk):
        try:
            Proposal.objects.get(pk=pk).delete()
        except Exception:
            raise ParseError(_(f"{pk} is not found."),
                             code='proposal_not_found')

        return Response(status=HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        try:
            proposal = Proposal.objects.get(pk=pk)
        except Exception:
            raise ParseError(_(f'{pk} is invalid proposal id.'),
                             code='invalid_proposal_id')

        serilaizer = ProposalDetailsSerializer(
            instance=proposal, data=request.data, partial=True, context={'request': request})
        serilaizer.is_valid(raise_exception=True)
        serilaizer.save()

        responce_serializer = ProposalSerializer(
            proposal, context={'request': request})

        return Response(responce_serializer.data, status=HTTP_201_CREATED)


##
# Filters
##


class FiltersAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            categories = Category.objects.all()
            cities = City.objects.all()

            serializer = FiltersSerializer(
                instance={'categories': categories, 'cities': cities})

        except Exception:
            raise ParseError(_("Can't get filters"),
                             code='can_not_get_filters')

        return Response(serializer.data, status=HTTP_200_OK)
