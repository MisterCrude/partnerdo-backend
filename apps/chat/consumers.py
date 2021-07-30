import asyncio

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
def reset_unread_message_number(chatroom_id, user_id):
    try:
        chatroom = Chatroom.objects.filter(
            id=chatroom_id)

        if chatroom.filter(initiator__id=user_id).count():
            chatroom.update(unread_message_number_for_initiator=0)
        else:
            chatroom.update(unread_message_number_for_proposal_author=0)

    except Exception:
        return None


@database_sync_to_async
def get_message_list(chatroom_id, amount=10):
    try:
        messages = Message.objects.order_by(
            '-created').filter(chatroom_id=chatroom_id)
        message_slice = messages[:amount]
        serializer = MessageSerializer(reversed(message_slice), many=True)

        return serializer.data
    except Exception:
        return None


@database_sync_to_async
def get_chatroom_list_and_nonification(user):
    try:
        chatrooms = Chatroom.objects.filter(
            Q(initiator=user) | Q(proposal_author=user))
        serializer = ChatroomSerializer(chatrooms, many=True)
        chatroom_list = []
        notifaication_list = []

        for item in serializer.data:
            chatroom = dict(item)
            proposal_author_message_number = float(
                chatroom['unread_message_number_for_proposal_author'])
            initiator_message_number = float(
                chatroom['unread_message_number_for_initiator'])
            proposal_author_id = dict(chatroom['proposal_author'])['id']

            if proposal_author_id == str(user.id):
                chatroom['unread_message_number'] = proposal_author_message_number
                notifaication_list.append(proposal_author_message_number > 0)
            else:
                chatroom['unread_message_number'] = initiator_message_number
                notifaication_list.append(initiator_message_number > 0)

            del chatroom['unread_message_number_for_proposal_author']
            del chatroom['unread_message_number_for_initiator']

            chatroom_list.append(chatroom)

        return chatroom_list, True in notifaication_list
    except Exception:
        return None, None


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        self.room_group_name = f'user_{self.user.id}'

        if self.user.is_anonymous:
            return await self.close()

        await self.accept()

        chatrooms, hasNotification = await get_chatroom_list_and_nonification(self.user)

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )

        if hasNotification:
            # Run async tasks concurrently
            await asyncio.gather(
                self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'message': chatrooms,
                        'type': MESSAGE_TYPE_LIST['CHATROOM_LIST'],
                    }),
                self.group_send_has_notification(self.room_group_name)
            )
        else:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'message': chatrooms,
                    'type': MESSAGE_TYPE_LIST['CHATROOM_LIST'],
                }),

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name,
        )

    async def receive_json(self, content):
        # CONNECT TO CHATROOM
        if content['type'] == MESSAGE_TYPE_LIST['CONNECT_TO_CHATROOM']:
            chatroom_id = content['message']
            room_group_name = f'message_list_{chatroom_id}'

            message_list = await get_message_list(chatroom_id)

            await self.channel_layer.group_add(
                room_group_name,
                self.channel_name
            )

            await asyncio.gather(
                reset_unread_message_number(chatroom_id, self.user.id),
                self.channel_layer.group_send(
                    room_group_name,
                    {
                        'message': message_list,
                        'type': MESSAGE_TYPE_LIST['CHATROOM_MESSAGE_LIST'],
                    })
            )

        # NEW CHAROOM MESSAGE
        if content['type'] == MESSAGE_TYPE_LIST['NEW_CHATROOM_MESSAGE']:
            chatroom_id = content['message']['chatroom_id']
            new_message = content['message']['text']

            # TODO refactor it
            chatroom_instance_list = await database_sync_to_async(Chatroom.objects.filter)(pk=chatroom_id)
            chatroom_instance = await database_sync_to_async(chatroom_instance_list.get)()
            chat_participant = await database_sync_to_async(chatroom_instance_list.values_list)('proposal_author', 'initiator')

            chat_participant_list = await database_sync_to_async(list)(chat_participant)
            proposal_author_id, initiator_id = chat_participant_list[
                0][0], chat_participant_list[0][1]

            participant_group_name = f'user_{proposal_author_id}' if self.user.id == initiator_id else f'user_{initiator_id}'
            room_group_name = f'message_list_{chatroom_id}'

            await database_sync_to_async(Message.objects.create)(
                content=new_message, author=self.user, chatroom=chatroom_instance)

            message_list = await get_message_list(chatroom_id)

            # Run async tasks concurrently
            await asyncio.gather(
                self.channel_layer.group_send(
                    room_group_name,
                    {
                        'type': MESSAGE_TYPE_LIST['CHATROOM_MESSAGE_LIST'],
                        'message': message_list,
                    }),
                self.group_send_has_notification(participant_group_name)
            )

    async def group_send_has_notification(self, room_group_name):
        await self.channel_layer.group_send(
            room_group_name,
            {
                'type': MESSAGE_TYPE_LIST['HAS_NOTIFICATION'],
            })

    ##
    # Message types
    # -------------
    # intercept messages sended to the group
    # and triggers WebSocket message
    ##

    # TODO merge it
    async def chatroom_list(self, event):
        message = event['message']
        message_type = event['type']

        await self.send_json({
            'type': message_type,
            'message': message,
        })

    async def chatroom_message_list(self, event):
        message = event['message']
        message_type = event['type']

        await self.send_json({
            'message': message,
            'type': message_type,
        })

    async def has_notification(self, event):
        message_type = event['type']

        await self.send_json({
            'type': message_type,
        })
