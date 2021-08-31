from django.db.models import Q
from django.utils.translation import gettext as _
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView

from apps.proposal.models import Proposal

from .constants import STATUS_TYPE
from .models import Chatroom
from .serializers import ChatroomCreateSerializer
from .utils import prepare_chatroom_serializer

##
# Chat room
##


class ChatroomDetailsAPIView(APIView):
    def get(self, request, pk):
        try:
            user = request.user
            proposal_response = Chatroom.objects.get(
                Q(pk=pk), Q(initiator=user) | Q(proposal_author=user))
            chatroom_serialized_data = prepare_chatroom_serializer(
                proposal_response, user.id)
        except Exception:
            raise ParseError(_(f"{pk} is invalid chat room id."),
                             code='invalid_chatroom_id')

        return Response(chatroom_serialized_data, status=HTTP_200_OK)


class ChatroomCreateAPIView(APIView):
    def post(self, request):
        body_query_dict = request.data

        # Check if all required fields have been sent
        if not body_query_dict.get('initial_message'):
            raise ParseError(_("Request doesn't contain initial_message field"),
                             code='message_field_does_not_exist')

        if not body_query_dict.get('initiator'):
            raise ParseError(_("Request doesn't contain initiator field"),
                             code='initiator_field_does_not_exist')

        if not body_query_dict.get('proposal'):
            raise ParseError(_("Request doesn't contain proposal field"),
                             code='proposal_field_does_not_exist')

        proposal = Proposal.objects.get(pk=body_query_dict.get('proposal'))
        initiator_id = str(body_query_dict.get('initiator'))

        # Can't respond to same proposal twice
        if Chatroom.objects.filter(Q(initiator__id=initiator_id), Q(id=proposal.id)).exists():
            raise ParseError(_("Can't respond to same proposal twice"),
                             code='can_not_respond_twice_for_same_proposal')

        # Initiator can't be proposal author
        if str(proposal.author.id) == initiator_id:
            raise ParseError(
                _("Initiator and proposol author can't be the same user"), code='proposal_and_author_same_user')

        try:
            serializer = ChatroomCreateSerializer(
                data=body_query_dict)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=HTTP_201_CREATED)
        except Exception:
            raise ParseError(_("Can't create new chat room"),
                             code='can_not_create_chatroom')


class ChatroomChangeStatusAPIView(APIView):
    _approve_status = STATUS_TYPE['APPROVED']
    _reject_status = STATUS_TYPE['REJECTED']

    def get(self, request, pk, status):
        # Check status
        if status != self._approve_status and status != self._reject_status:
            raise ParseError(_('Status should be "AP - approved" or "RJ - rejected"'),
                             code="cant_change_proposal_response_status")

        try:
            chatroom = Chatroom.objects.get(pk=pk)

            # Avoid changing status twice for same chatroom
            if chatroom.status != STATUS_TYPE['IDLE']:
                raise ParseError()

            # Accept changing only from proposal author
            if chatroom.proposal_author.id != request.user.id:
                # No need to add description, because error will catchend in except block
                raise ParseError()

            serializer = ChatroomCreateSerializer(
                instance=chatroom, data={'status': status}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=HTTP_200_OK)
        except Exception:
            raise ParseError(_("Can't change status"),
                             code="can_not_change_chatroom_open_status")
