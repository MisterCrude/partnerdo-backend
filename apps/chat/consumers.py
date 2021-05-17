import datetime
import json

from channels.generic.websocket import AsyncWebsocketConsumer

from apps.profile.serializers import ProfileSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']

        if not user.is_anonymous:
            self.user = dict(ProfileSerializer(user).data)
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_%s' % self.room_name

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
        else:
            await self.close()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'created': datetime.datetime.now().__str__(),
                'message': message,
                'type': 'chatroom_message',
                'user': self.user.get('id'),
            }
        )

    async def chatroom_message(self, event):
        created = event['created']
        message = event['message']
        message_type = event['type']
        user = event['user']

        await self.send(text_data=json.dumps({
            'created': created,
            'message': message,
            'type': message_type,
            'user': user,
        }))
