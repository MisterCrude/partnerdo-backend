from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.db.models import Q

from .constants import MESSAGE_TYPE_LIST
from .models import Chatroom, Message
from .serializers import ChatroomSerializer, MessageSerializer


@database_sync_to_async
def get_chatroom_satus(user, chatroom_id):
    try:
        return Chatroom.objects.values_list('status').get(
            Q(pk=chatroom_id), Q(initiator=user) | Q(proposal_author=user))[0]
    except Exception:
        return None


@database_sync_to_async
def get_chatroom_messages(chatroom_id, amount=10):
    try:
        messages = Message.objects.order_by(
            '-created').filter(chatroom_id=chatroom_id)
        message_slice = messages[:amount]
        serializer = MessageSerializer(reversed(message_slice), many=True)

        return serializer.data
    except Exception:
        return None


@database_sync_to_async
def get_chatrooms(user):
    try:
        chatrooms = Chatroom.objects.filter(
            Q(initiator=user) | Q(proposal_author=user))
        serializer = ChatroomSerializer(chatrooms, many=True)

        return serializer.data
    except Exception:
        return None


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']

        if self.user.is_anonymous:
            return await self.close()

        await self.accept()

        chatrooms = await get_chatrooms(self.user)

        # Send chatrooms
        room_group_name = f'user_{self.user.id}'
        await self.channel_layer.group_add(
            room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            room_group_name,
            {
                'message': chatrooms,
                'type': MESSAGE_TYPE_LIST['CHATROOM_LIST'],
            })

    async def receive_json(self, content):
        if content['type'] == MESSAGE_TYPE_LIST['CONNECT_TO_CHATROOM']:
            chatroom_id = content['message']
            room_group_name = f'chatroom_message_list_{chatroom_id}'

            print(111)

            await self.channel_layer.group_add(
                room_group_name,
                self.channel_name
            )

            await self.channel_layer.group_send(
                room_group_name,
                {
                    'message': await get_chatroom_messages(chatroom_id),
                    'type': MESSAGE_TYPE_LIST['CHATROOM_MESSAGE_LIST'],
                })

        if content['type'] == MESSAGE_TYPE_LIST['NEW_CHATROOM_MESSAGE']:
            chatroom_id = content['message']['chatroom_id']
            new_message = content['message']['text']
            room_group_name = f'chatroom_message_list_{chatroom_id}'
            chatroom_instance = await database_sync_to_async(Chatroom.objects.get)(pk=chatroom_id)

            await database_sync_to_async(Message.objects.create)(
                content=new_message, author=self.user, chatroom=chatroom_instance)

            await self.channel_layer.group_send(
                room_group_name,
                {
                    'message': await get_chatroom_messages(chatroom_id),
                    'type': MESSAGE_TYPE_LIST['CHATROOM_MESSAGE_LIST'],
                })

    ##
    # Message types
    # -------------
    # intercept messages sended to the group
    # and triggers WebSocket message
    ##

    async def chatroom_list(self, event):
        message = event['message']
        message_type = event['type']

        await self.send_json({
            'message': message,
            'type': message_type,
        })

    async def chatroom_message_list(self, event):
        message = event['message']
        message_type = event['type']

        await self.send_json({
            'message': message,
            'type': message_type,
        })

    async def has_new_message(self, event):
        message_type = event['type']

        await self.send_json({
            'type': message_type,
        })
