from django.contrib import admin

from .models import Chatroom, Message


class MessgesInline(admin.TabularInline):
    readonly_fields = ['author']
    fields = ['id', 'author', 'content']
    model = Message
    extra = 0


@admin.register(Chatroom)
class ChatroomAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'last_message',
                       'created', 'proposal_author']
    fieldsets = (
        (None, {
            'fields': ('id', 'status', 'proposal',  'proposal_author',
                       'initiator', 'initial_message', 'unread_message_number_for_proposal_author', 'unread_message_number_for_initiator')
        }),
        ('Dates', {
            'fields': ('last_message', 'created',),
        }),
    )

    inlines = [MessgesInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'created']
    fields = ('id', 'author', 'chatroom', 'content', 'created')
