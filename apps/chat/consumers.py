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


# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope['user']
#         self.chatroom_id = self.scope['url_route']['kwargs']['chatroom_id']
#         self.chatroom_status = await get_chatroom_satus(self.user, self.chatroom_id)

#         self.room_group_name = 'chat_%s' % self.chatroom_id

#         if self.user.is_anonymous:
#             return await self.close()

#         if not self.chatroom_status and self.chatroom_status != 1:
#             return await self.close()

#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         await self.accept()
#         await self.send_message_to_group()

#     async def disconnect(self, close_code):
#         if not self.user.is_anonymous:
#             await self.channel_layer.group_discard(
#                 self.room_group_name,
#                 self.channel_name
#             )

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']

#         try:
#             chatroom_instance = await database_sync_to_async(Chatroom.objects.get)(pk=self.chatroom_id)

#             await database_sync_to_async(Message.objects.create)(
#                 content=message, author=self.user, chatroom=chatroom_instance)

#             await self.send_message_to_group()
#         except Exception:
#             return await self.close()

#     ##
#     # Message types
#     ##

#     async def send_chatroom_message_list(self, event):
#         message = event['message']
#         message_type = event['type']

#         await self.send(json.dumps({
#             'message': message,
#             'type': message_type,
#         }))

#     ##
#     # Utils
#     ##

    # async def send_message_to_group(self):
    #     await self.channel_layer.group_send(
    #         self.room_group_name,
    #         {
    #             'message': await get_chatroom_messages(self.chatroom_id),
    #             'type': MESSAGE_TYPE_LIST.get('SEND_CHATROOM_MESSAGE_LIST'),
    #         }
    #     )


class ChatConsumerTest(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']

        if self.user.is_anonymous:
            return await self.close()

        await self.accept()

        chatrooms = await get_chatrooms(self.user)

        # Send chatrooms
        room_group_name = f'chatroom_list_{self.user.id}'
        await self.channel_layer.group_add(
            room_group_name,
            self.channel_name
        )

        await self.channel_layer.group_send(
            room_group_name,
            {
                'message': chatrooms,
                'type': MESSAGE_TYPE_LIST.get('CHATROOM_LIST'),
            })

    async def receive_json(self, content):
        # text_data_json = json.loads(text_data)
        # message = text_data_json['message']

        if content.get('type') == MESSAGE_TYPE_LIST.get('CONNECT_TO_CHATROOM'):
            self.chatroom_id = content.get('message')
            room_group_name = f'chatroom_message_list_{self.chatroom_id}'

            await self.channel_layer.group_add(
                room_group_name,
                self.channel_name
            )

            await self.channel_layer.group_send(
                room_group_name,
                {
                    'message': await get_chatroom_messages(self.chatroom_id),
                    'type': MESSAGE_TYPE_LIST.get('CHATROOM_MESSAGE_LIST'),
                })

        if content.get('type') == MESSAGE_TYPE_LIST.get('NEW_CHATROOM_MESSAGE'):
            chatroom_id = self.chatroom_id
            # chatroom_instance = await database_sync_to_async(Chatroom.objects.get)(pk=chatroom_id)
            # new_message = content.get('message')

            # await database_sync_to_async(Message.objects.create)(
            #     content=new_message, author=self.user, chatroom=chatroom_instance)

            # await self.channel_layer.group_send(
            #     room_group_name,
            #     {
            #         'message': await get_chatroom_messages(chatroom_id),
            #         'type': MESSAGE_TYPE_LIST.get('CHATROOM_MESSAGE_LIST'),
            #     })

            print(111, chatroom_id)

    ##
    # Message types
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


# connect user
# send his chatrooms
