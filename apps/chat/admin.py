from django.contrib import admin

from .models import ChatRoom


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'last_message',
                       'chatroom', 'created', 'proposal_author']
    fieldsets = (
        (None, {
            'fields': ('id', 'chatroom', 'status', 'proposal',  'proposal_author', 'initiator', 'initial_message', 'unread_message_number')
        }),
        ('Dates', {
            'fields': ('last_message', 'created',),
        }),
    )
