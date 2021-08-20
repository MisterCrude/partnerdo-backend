
from rest_framework import serializers

from apps.proposal.serializers import AuthorSerializer, ProposalSerializer

from .models import Chatroom, Message

##
# Chat room
##


class ChatroomAuthorSerializer(AuthorSerializer):
    class Meta(AuthorSerializer.Meta):
        fields = ('id', 'username', 'first_name', 'last_name', 'avatar', )


class ChatroomProposalSerializer(ProposalSerializer):
    class Meta(ProposalSerializer.Meta):
        exclude = ('updated', 'description', 'created')


class ChatroomSerializer(serializers.ModelSerializer):
    initiator = ChatroomAuthorSerializer()
    proposal_author = ChatroomAuthorSerializer()
    proposal = ChatroomProposalSerializer()
    message_total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Chatroom
        exclude = ('_is_status_changed',)

    def get_message_total_amount(self, obj):
        return obj.messages.count()


class ChatroomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        extra_kwargs = {'proposal_author': {'required': False}}
        fields = '__all__'
        model = Chatroom


##
# Message
##

class MessageSerializer(serializers.ModelSerializer):
    author = ChatroomAuthorSerializer()

    class Meta:
        fields = '__all__'
        model = Message

    def to_representation(self, obj):
        author = {
            "id": str(obj.author.id),
            "username": obj.author.username,
            "first_name": obj.author.first_name,
            "last_name": obj.author.last_name
        }

        return {
            "id": str(obj.id),
            "content": obj.content,
            "created": str(obj.created),
            "author": author,
            "chatroom": str(obj.chatroom)
        }
