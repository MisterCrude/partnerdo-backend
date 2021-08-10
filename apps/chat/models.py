import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext as _

from .constants import (INITIATOR_NOTIFICATION_TYPE_CHOISE, NOTIFICATION_TYPE,
                        PROPOSAL_AUTHOR_NOTIFICATION_TYPE_CHOISE,
                        STATUS_CHOISE)


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    content = models.TextField(max_length=400)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='message_author', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    chatroom = models.ForeignKey(
        'Chatroom', related_name='messages', on_delete=models.CASCADE)
    is_unread = models.BooleanField(default=True)

    def clean(self):
        chatroom_initiator = self.chatroom.initiator
        chatroom_proposal_author = self.chatroom.proposal_author

        if self.author.id not in [chatroom_initiator.id, chatroom_proposal_author.id]:
            raise ValidationError(
                _('Author should be chat room initiator or proposal author'))

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self._state.adding:
            chatroom_object_list = Chatroom.objects
            initiator = chatroom_object_list.values_list(
                'initiator', flat=True).get(id=self.chatroom.id)
            filtered = chatroom_object_list.filter(id=self.chatroom.id)

            if initiator == self.author:
                filtered.update(
                    proposal_author_notification_type=NOTIFICATION_TYPE['NEW_MESSAGE'])
            else:
                filtered.update(
                    initiator_notification_type=NOTIFICATION_TYPE['NEW_MESSAGE'])

        super(Message, self).save(*args, **kwargs)


class Chatroom(models.Model):
    _is_status_changed = models.BooleanField(default=False, editable=False)

    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    initiator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='chatroom_initiator',
                                  on_delete=models.PROTECT)
    proposal_author = models.ForeignKey(settings.AUTH_USER_MODEL,
                                        related_name='chatroom_author',
                                        on_delete=models.PROTECT)
    proposal = models.ForeignKey('proposal.Proposal',
                                 related_name='chatrooms',
                                 on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOISE, default=0)
    last_message = models.DateTimeField(auto_now_add=True,
                                        help_text="Date of the last message")
    created = models.DateTimeField(auto_now_add=True)
    initial_message = models.TextField(max_length=400)
    initiator_notification_type = models.CharField(choices=INITIATOR_NOTIFICATION_TYPE_CHOISE,
                                                   default=NOTIFICATION_TYPE['IDLE'],
                                                   max_length=2)
    proposal_author_notification_type = models.CharField(choices=PROPOSAL_AUTHOR_NOTIFICATION_TYPE_CHOISE,
                                                         default=NOTIFICATION_TYPE['IDLE'],
                                                         max_length=2)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self._state.adding:
            self.proposal_author = self.proposal.author
            self.proposal_author_notification_type = NOTIFICATION_TYPE['CREATE_CHATROOM']

        if not self._state.adding and not self._is_status_changed and self.status != 0:
            self.proposal_author_notification_type = NOTIFICATION_TYPE['CHANGE_STATUS']

        super(Chatroom, self).save(*args, **kwargs)
