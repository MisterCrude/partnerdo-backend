
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .constants import MESSAGE_TYPE_LIST
from .consumers import get_chatroom_list_and_nonification_type
from .models import Chatroom

# @receiver(post_save, sender=Chatroom)
# def change_staus_handler(instance, **kwargs):
# Is new satatus approve or reject
# if instance.has_status_notification:
#     channel_layer = get_channel_layer()
#     room_group_name = f'user_{instance.initiator.id}'

#     chatroom_list, has_notification = get_chatroom_list_and_nonification(
#         instance.proposal_author.id)

#     async_to_sync(channel_layer.group_send)(
#         room_group_name,
#         {
#             'message': {
#                 "chatroom_list": chatroom_list,
#                 "has_notification": has_notification
#             },
#             'type': MESSAGE_TYPE_LIST['CHATROOM_LIST'],
#         },
#     )


@receiver(post_save, sender=Chatroom)
def create_chatroom_handler(instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        room_group_name = f'user_{instance.proposal_author.id}'

        chatroom_list, has_notification = get_chatroom_list_and_nonification_type(
            instance.proposal_author.id)

        async_to_sync(channel_layer.group_send)(
            room_group_name,
            {
                'message': {
                    "chatroom_list": chatroom_list,
                    "has_notification": has_notification
                },
                'type': MESSAGE_TYPE_LIST['CHATROOM_LIST'],
            }),
