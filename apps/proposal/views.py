from rest_framework import viewsets

from .serializers import ProposalSerializer
from .models import Proposal


class ProposalViewSet(viewsets.ModelViewSet):
    #  permission_classes = (IsAccountAdminOrReadOnly,)
    queryset = Proposal.objects.all().order_by('name')
    serializer_class = ProposalSerializer
