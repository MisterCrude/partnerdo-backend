from django.utils.translation import ugettext as _

MESSAGE_TYPE_LIST = {
    'CHATROOM_LIST': 'chatroom_list',
    'MESSAGE_LIST': 'message_list',
    'CONNECT_TO_CHATROOM': 'connect_to_chatroom',
    'CHATROOM_MESSAGE': 'chatroom_message',
    'CHATROOM_STATUS': 'chatroom_status',
    'NOTIFICATION_TYPE': 'notification_type'
}

STATUS_CHOISE = [
    (0, _('Idle')),
    (1, _('Approved')),
    (2, _('Rejected')),
]

NOTIFICATION_TYPE = {
    'IDLE': 'ID',
    'NEW_MESSAGE': 'NM',
    'CHANGE_STATUS': 'CS',
    'CREATE_CHATROOM': 'CM',
}

INITIATOR_NOTIFICATION_TYPE_CHOISE = [
    (NOTIFICATION_TYPE['CHANGE_STATUS'], _('Change status')),
    (NOTIFICATION_TYPE['IDLE'], _('Idle')),
    (NOTIFICATION_TYPE['NEW_MESSAGE'], _('New message')),
]

PROPOSAL_AUTHOR_NOTIFICATION_TYPE_CHOISE = [
    (NOTIFICATION_TYPE['CHANGE_STATUS'], _('Change status')),
    (NOTIFICATION_TYPE['IDLE'], _('Idle')),
    (NOTIFICATION_TYPE['NEW_MESSAGE'], _('New message')),
    (NOTIFICATION_TYPE['CREATE_CHATROOM'], _('Create chatroom')),
]
