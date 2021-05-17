
from rest_framework import serializers

from apps.proposal.serializers import AuthorSerializer, ProposalSerializer

from .models import ChatRoom

##
# Chat room
##


class ChatRoomAuthorSerializer(AuthorSerializer):
    class Meta(AuthorSerializer.Meta):
        fields = ('id', 'username', 'first_name', 'last_name', 'avatar', )


class ChatRoomProposalSerializer(ProposalSerializer):
    author = None

    class Meta(ProposalSerializer.Meta):
        exclude = ('updated', 'description', 'author', 'created')


class ChatRoomSerializer(serializers.ModelSerializer):
    initiator = ChatRoomAuthorSerializer()
    proposal_author = ChatRoomAuthorSerializer()
    proposal = ChatRoomProposalSerializer()

    class Meta:
        model = ChatRoom
        fields = '__all__'


class ChatRoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {'proposal_author': {'required': False}}
        fields = '__all__'
        model = ChatRoom
