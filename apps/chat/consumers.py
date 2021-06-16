import datetime
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import Q

from .models import ChatRoom


@database_sync_to_async
def get_chat_room(user, chat_room_id):
    try:
        return ChatRoom.objects.values_list('status').get(
            Q(pk=chat_room_id), Q(initiator=user) | Q(proposal_author=user))
    except Exception:
        return None


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.chat_room_id = self.scope['url_route']['kwargs']['chat_room_id']
        self.room_group_name = 'chat_%s' % self.chat_room_id
        self.chat_room = await get_chat_room(self.user, self.chat_room_id)

        if not self.chat_room:
            return await self.close()

        if self.user.is_anonymous:
            return await self.close()

        # If not approved
        if self.chat_room[0] != 1:
            return await self.close()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        return await self.accept()

    async def disconnect(self, close_code):
        if not self.user.is_anonymous:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        sender = {
            'id': str(self.user.id),
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'username': self.user.username,
        }

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'created': str(datetime.datetime.now()),
                'message': message,
                'type': 'chatroom_message',
                'sender': sender,
            }
        )

    async def chatroom_message(self, event):
        created = event['created']
        message = event['message']
        message_type = event['type']
        sender = event['sender']

        await self.send(text_data=json.dumps({
            'created': created,
            'message': message,
            'type': message_type,
            'sender': sender,
        }))
