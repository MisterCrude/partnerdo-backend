from django.http import Http404
from drf_multiple_model.views import ObjectMultipleModelAPIView
from rest_framework import viewsets, generics, views, response, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Proposal, City, Category
from .serializers import ProposalSerializer, CitySerializer, CategorySerializer


class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer

    def retrive(self, request, pk=None):
        queryset = Proposal.objects.all()
        proposal = get_object_or_404(queryset, pk=pk)
        serializer = ProposalSerializer(proposal)
        return Response(serializer.data)


class ProposalDetails(views.APIView):
    def get_object(self, id):
        try:
            return Proposal.objects.get(pk=id)
        except Proposal.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        proposal = self.get_object(pk)
        serializer = ProposalSerializer(proposal)
        return response.Response(serializer.data)

    def delete(self, request, pk, format=None):
        proposal = self.get_object(pk)
        proposal.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


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


""" 
GET 
- retrive list with pagination

POST
- create proposal in custom way

PUT
- update fields few fields or create new one

"""
