import uuid

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _

from .constants import MESSAGE_TYPE_LIST

CHATROOM_OPEN_STATUS = [
    (0, _('Idle')),
    (1, _('Approved')),
    (2, _('Rejected')),
]


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    content = models.TextField(max_length=400)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='message_author', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    chatroom = models.ForeignKey(
        'Chatroom', related_name='messages', on_delete=models.CASCADE)

    def clean(self):
        chatroom_initiator = self.chatroom.initiator
        chatroom_proposal_author = self.chatroom.proposal_author

        if self.author.id not in [chatroom_initiator.id, chatroom_proposal_author.id]:
            raise ValidationError(
                _('Author should be chat room initiator or proposal author'))

    def __str__(self):
        return str(self.id)


class Chatroom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    initiator = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='chatroom_initiator', on_delete=models.PROTECT)
    proposal_author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='chatroom_author', on_delete=models.PROTECT)
    proposal = models.ForeignKey(
        'proposal.Proposal', related_name='chatrooms', on_delete=models.CASCADE)
    status = models.IntegerField(choices=CHATROOM_OPEN_STATUS, default=0)
    last_message = models.DateTimeField(
        auto_now_add=True, help_text="Date of the last message")
    created = models.DateTimeField(auto_now_add=True)
    initial_message = models.TextField(max_length=400)
    unread_message_number = models.DecimalField(
        default=0, decimal_places=0, max_digits=10, validators=[MinValueValidator(0)])

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):

        # Run only when create model instance
        if self._state.adding:
            # Set proposal author
            self.proposal_author = self.proposal.author

        super(Chatroom, self).save(*args, **kwargs)


##
# Signals
##

@receiver(post_save, sender=Chatroom)
def change_staus_handler(instance, **kwargs):
    # Is new satatus approve or reject
    if instance.status != 0:
        channel_layer = get_channel_layer()
        room_group_name = f'user_{instance.initiator.id}'

        async_to_sync(channel_layer.group_send)(
            room_group_name,
            {
                'type': MESSAGE_TYPE_LIST['HAS_NEW_MESSAGE'],
            }
        )


@receiver(post_save, sender=Chatroom)
def create_chatroom_handler(instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        room_group_name = f'user_{instance.proposal_author.id}'

        # 2. Add channel name

        async_to_sync(channel_layer.group_send)(
            room_group_name,
            {
                'type': MESSAGE_TYPE_LIST['HAS_NEW_MESSAGE'],
            }
        )
