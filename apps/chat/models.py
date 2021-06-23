import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _

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
    chatroom = models.UUIDField(default=uuid.uuid4)
    last_message = models.DateTimeField(
        auto_now_add=True, help_text="Date of the last message")
    created = models.DateTimeField(auto_now_add=True)
    initial_message = models.TextField(max_length=400)
    unread_message_number = models.DecimalField(
        default=0, decimal_places=0, max_digits=10, validators=[MinValueValidator(0)])

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ('-created',)


##
# Signals
##


@receiver(pre_save, sender=Chatroom)  # sender will be class
def proposal_response_save_handler(sender, instance, raw, using, update_fields, **kwargs):
    instance.proposal_author = instance.proposal.author
