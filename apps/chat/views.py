from django.db.models import Q
from django.utils.translation import gettext as _
from rest_framework.exceptions import ParseError
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.views import APIView

from apps.proposal.models import Proposal

from .models import ChatRoom
from .serializers import ChatRoomCreateSerializer, ChatRoomSerializer

##
# Chat room
##


class ChatRoomListAPIView(ListAPIView):
    # Only for GET pagginated list
    serializer_class = ChatRoomSerializer

    def get_queryset(self):
        user = self.request.user
        return ChatRoom.objects.filter(Q(initiator=user) | Q(proposal_author=user))


class ChatRoomDetailsAPIView(APIView):
    def get(self, request, pk):
        try:
            user = self.request.user
            proposal_response = ChatRoom.objects.get(
                Q(pk=pk), Q(initiator=user) | Q(proposal_author=user))
            serializer = ChatRoomSerializer(
                proposal_response, context={'request': request})
        except Exception:
            raise ParseError(_(f"{pk} is invalid chat room id."),
                             code='invalid_chat_room_id')

        return Response(serializer.data, status=HTTP_200_OK)


class ChatRoomCreateAPIView(APIView):
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
        if ChatRoom.objects.filter(initiator__id=initiator_id).exists():
            raise ParseError(_("Can't respond to same proposal twice"),
                             code='can_not_respond_twice_for_same_proposal')

        # Initiator can't be proposal author
        if str(proposal.author.id) == initiator_id:
            raise ParseError(
                _("Initiator and proposol author can't be the same user"), code='proposal_and_author_same_user')

        try:
            serializer = ChatRoomCreateSerializer(
                data=body_query_dict)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=HTTP_201_CREATED)
        except Exception:
            raise ParseError(_("Can't create new chat room"),
                             code='can_not_create_chat_room')


class ChatRoomChangeStatusAPIView(APIView):
    _approve_status = 'approve'
    _reject_status = 'reject'

    def getStatusIndex(self, status):
        if status == self._approve_status:
            return 1
        elif status == self._reject_status:
            return 2
        return 0

    def get(self, request, pk, status):
        # Check status
        if status != self._approve_status and status != self._reject_status:
            raise ParseError(_('Status should be "approve" or "reject"'),
                             code="cant_change_proposal_response_status")

        try:
            chat_room = ChatRoom.objects.get(pk=pk)

            # Avoid changing status twice for same chat_room
            if chat_room.status != 0:
                # This error will chatched in except case
                raise ParseError()

            # User which send request can't be author of proposal response (chat room)
            if chat_room.initiator.id == request.user.id:
                # This error will chatched in except case
                raise ParseError()

            serializer = ChatRoomCreateSerializer(
                instance=chat_room, data={'status': self.getStatusIndex(status)}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=HTTP_200_OK)
        except Exception:
            raise ParseError(_("Can't change status"),
                             code="can_not_change_chat_room_open_status")
