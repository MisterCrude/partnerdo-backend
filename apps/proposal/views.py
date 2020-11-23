from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import ProposalSerializer
from .models import Proposal


class ProposalViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]

    queryset = Proposal.objects.all().order_by('name')
    serializer_class = ProposalSerializer
