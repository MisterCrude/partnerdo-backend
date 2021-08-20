from .constants import NOTIFICATION_TYPE
from .serializers import ChatroomSerializer


def prepare_chatroom_serializer(chatroom,  user_id):
    chatroom_serializer = ChatroomSerializer(chatroom)
    chatroom_data = dict(chatroom_serializer.data)

    proposal_author_id = dict(chatroom_data['proposal_author'])['id']
    initiator_id = dict(chatroom_data['initiator'])['id']

    unread_message_amount = 0
    companion = chatroom_data['initiator']
    notification_type = NOTIFICATION_TYPE['IDLE']

    # count unread messages and get notification type for current user
    if proposal_author_id == str(user_id):
        notification_type = chatroom_data['proposal_author_notification_type']
        unread_message_amount = chatroom.messages.filter(
            is_unread=True, author__id=initiator_id).count()

    if initiator_id == str(user_id):
        companion = chatroom_data['proposal_author']
        notification_type = chatroom_data['initiator_notification_type']
        unread_message_amount = chatroom.messages.filter(
            is_unread=True, author__id=proposal_author_id).count()

    del chatroom_data['proposal_author_notification_type']
    del chatroom_data['initiator_notification_type']
    del chatroom_data['proposal_author']
    del chatroom_data['initiator']

    chatroom_data['unread_message_amount'] = unread_message_amount
    chatroom_data['notification_type'] = notification_type
    chatroom_data['companion'] = companion

    return chatroom_data
