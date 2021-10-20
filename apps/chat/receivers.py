from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db.models.signals import post_save
from django.dispatch import receiver

from .constants import MESSAGE_TYPE_LIST, STATUS_TYPE
from .consumers import get_chatroom_list_and_nonification
from .models import Chatroom

"""
Change chatroom status
"""


@receiver(post_save, sender=Chatroom)
def change_staus_handler(instance, created, **kwargs):
    if not created and not instance._is_status_changed and instance.status != STATUS_TYPE['IDLE']:
        channel_layer = get_channel_layer()

        chatroom = Chatroom.objects.filter(id=instance.id)
        chatroom.update(_is_status_changed=True)

        # For proposal_author
        room_group_name = f'user_{instance.proposal_author.id}'
        chatroom_list, has_notification = get_chatroom_list_and_nonification(
            instance.proposal_author.id)

        async_to_sync(channel_layer.group_send)(
            room_group_name,
            {
                'message': {
                    "chatroom_list": chatroom_list,
                    "has_notification": has_notification
                },
                'type': MESSAGE_TYPE_LIST['CHATROOM_LIST'],
            },
        )

        # For initiator
        room_group_name = f'user_{instance.initiator.id}'
        chatroom_list, has_notification = get_chatroom_list_and_nonification(
            instance.initiator.id)

        async_to_sync(channel_layer.group_send)(
            room_group_name,
            {
                'message': {
                    "chatroom_list": chatroom_list,
                    "has_notification": has_notification
                },
                'type': MESSAGE_TYPE_LIST['CHATROOM_LIST'],
            },
        )

    if not created and instance._is_status_changed and instance.status == STATUS_TYPE['IDLE']:
        chatroom = Chatroom.objects.filter(id=instance.id)
        chatroom.update(_is_status_changed=False)


"""
Create chatroom
"""


@receiver(post_save, sender=Chatroom)
def create_chatroom_handler(instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        proposal_author_room_group_name = f'user_{str(instance.proposal_author.id)}'
        initiator_room_group_name = f'user_{str(instance.initiator.id)}'

        chatroom_list, has_notification = get_chatroom_list_and_nonification(
            instance.proposal_author.id)

        """
        Send for proposal author
        """
        async_to_sync(channel_layer.group_send)(proposal_author_room_group_name, {
            'message': {
                "chatroom_list": chatroom_list,
                "has_notification": has_notification
            },
            'type': MESSAGE_TYPE_LIST['CHATROOM_LIST'],
        })

        """
        Send for initiator
        """
        chatroom_list, has_notification = get_chatroom_list_and_nonification(
            instance.initiator.id)

        async_to_sync(channel_layer.group_send)(initiator_room_group_name, {
            'message': {
                "chatroom_list": chatroom_list,
                "has_notification": has_notification
            },
            'type': MESSAGE_TYPE_LIST['CHATROOM_LIST'],
        })
