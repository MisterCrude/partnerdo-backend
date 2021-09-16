import asyncio

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.core.cache import cache
from django.db.models import Q

from .constants import MESSAGE_TYPE_LIST, NOTIFICATION_TYPE, STATUS_TYPE
from .models import Chatroom, Message
from .serializers import MessageSerializer
from .utils import prepare_chatroom_serializer


def reset_unread_message_amount_and_status_notification(chatroom_id, user_id):
    try:
        chatroom_object_list = Chatroom.objects
        chatroom_filtered_queryset = chatroom_object_list.filter(
            id=chatroom_id)
        chatroom_queryset = chatroom_object_list.get(id=chatroom_id)

        initiator_id = Chatroom.objects.values_list(
            'initiator', flat=True).get(id=chatroom_id)

        if initiator_id == user_id:
            chatroom_filtered_queryset.update(
                initiator_notification_type=NOTIFICATION_TYPE['IDLE'])
        else:
            chatroom_filtered_queryset.update(
                proposal_author_notification_type=NOTIFICATION_TYPE['IDLE'])

        message_list_queryset = chatroom_queryset.messages.exclude(
            author=user_id)

        if message_list_queryset.count() > 0:
            for message_queryset in message_list_queryset:
                message = Message.objects.filter(id=message_queryset.id)
                message.update(is_unread=False)
    except Exception:
        return None


def get_message_list(chatroom_id, amount=10):
    try:
        messages = Message.objects.order_by(
            '-created').filter(chatroom_id=chatroom_id)
        message_slice = messages[:amount]
        serializer = MessageSerializer(reversed(message_slice), many=True)

        return serializer.data
    except Exception:
        return None


def get_participant_id_list(chatroom_id):
    try:
        chatroom_instance_list = Chatroom.objects.filter(pk=chatroom_id)
        chat_participant = chatroom_instance_list.values_list(
            'proposal_author', 'initiator')
        chat_participant_list = list(chat_participant)
        proposal_author_id, initiator_id = chat_participant_list[0][0], chat_participant_list[0][1]

        return proposal_author_id, initiator_id
    except Exception:
        return None


def get_chatroom_list_and_nonification(user_id):
    try:
        chatrooms = Chatroom.objects.filter(
            Q(initiator__id=user_id) | Q(proposal_author__id=user_id))
        chatroom_list = []
        notification_list = []

        for chatroom in chatrooms:
            chatroom_serialized_data = prepare_chatroom_serializer(
                chatroom, user_id)

            chatroom_list.append(chatroom_serialized_data)
            notification_list.append(
                chatroom_serialized_data['notification_type'] != NOTIFICATION_TYPE['IDLE'])

        has_notification = True in notification_list

        return chatroom_list, has_notification
    except Exception:
        return None, None


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.user_room_group_name = f'user_{self.user.id}'

        if self.user.is_anonymous:
            return await self.close()

        await self.accept()

        # Set logged_user_id global variable
        cache.set('logged_user_id', str(self.user.id))
        chatroom_list, has_notification = await database_sync_to_async(get_chatroom_list_and_nonification)(self.user.id)

        await self.channel_layer.group_add(
            self.user_room_group_name,
            self.channel_name,
        )

        await self.channel_layer.group_send(
            self.user_room_group_name,
            {
                'message': {
                    "chatroom_list": chatroom_list,
                    "has_notification": has_notification
                },
                'type': MESSAGE_TYPE_LIST['CHATROOM_LIST'],
            }),

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.user_room_group_name,
            self.channel_name,
        )

    async def receive_json(self, content):
        # CONNECT TO CHATROOM
        if content['type'] == MESSAGE_TYPE_LIST['CONNECT_TO_CHATROOM']:
            chatroom_id = content['message']
            room_group_name = f'message_list_{chatroom_id}'
            room_group_name = f'message_list_{chatroom_id}'

            message_list = await database_sync_to_async(get_message_list)(chatroom_id)
            proposal_author_id, initiator_id = await database_sync_to_async(get_participant_id_list)(chatroom_id)

            await database_sync_to_async(reset_unread_message_amount_and_status_notification)(chatroom_id, self.user.id)

            chatroom_list, has_notification = await database_sync_to_async(get_chatroom_list_and_nonification)(self.user.id)

            await self.channel_layer.group_add(
                room_group_name,
                self.channel_name
            )

            await asyncio.gather(
                self.channel_layer.group_send(
                    room_group_name,
                    {
                        'message': message_list,
                        'type': MESSAGE_TYPE_LIST['MESSAGE_LIST'],
                    }),
                self.channel_layer.group_send(
                    self.user_room_group_name,
                    {
                        'message': {
                            "chatroom_list": chatroom_list,
                            "has_notification": has_notification
                        },
                        'type': MESSAGE_TYPE_LIST['CHATROOM_LIST'],
                    }),
            )

        # CHAROOM MESSAGE
        if content['type'] == MESSAGE_TYPE_LIST['CHATROOM_MESSAGE']:
            chatroom_id = content['message']['chatroom_id']
            new_message = content['message']['text']

            chatroom_instance_list = await database_sync_to_async(Chatroom.objects.filter)(pk=chatroom_id)
            chatroom_instance = await database_sync_to_async(chatroom_instance_list.get)()

            # If satus dont changes don't allow send message
            if chatroom_instance.status == STATUS_TYPE['IDLE']:
                return None

            proposal_author_id, initiator_id = await database_sync_to_async(get_participant_id_list)(chatroom_id)

            participant_id = proposal_author_id if self.user.id == initiator_id else initiator_id
            participant_group_name = f'user_{participant_id}'
            room_group_name = f'message_list_{chatroom_id}'

            await database_sync_to_async(Message.objects.create)(
                content=new_message, author=self.user, chatroom=chatroom_instance)

            message_list = await database_sync_to_async(get_message_list)(chatroom_id)
            chatroom_list, has_notification = await database_sync_to_async(get_chatroom_list_and_nonification)(participant_id)

            # Run async tasks concurrently
            await asyncio.gather(
                self.channel_layer.group_send(
                    room_group_name,
                    {
                        'type': MESSAGE_TYPE_LIST['MESSAGE_LIST'],
                        'message': message_list,
                    }),
                self.channel_layer.group_send(
                    participant_group_name,
                    {
                        'message': {
                            "chatroom_list": chatroom_list,
                            "has_notification": has_notification
                        },
                        'type': MESSAGE_TYPE_LIST['CHATROOM_LIST'],
                    }),
            )

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
            'type': message_type,
            'message': message,
        })

    async def message_list(self, event):
        message = event['message']
        message_type = event['type']

        await self.send_json({
            'message': message,
            'type': message_type,
        })
