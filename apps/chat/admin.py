from django.contrib import admin

from .models import Chatroom, Message


class MessgesInline(admin.TabularInline):
    fields = ['id', 'is_unread', 'author', 'content']

    model = Message
    extra = 0


@admin.register(Chatroom)
class ChatroomAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'last_message', 'created', 'proposal_author']
    fieldsets = (
        (None, {
            'fields': ('id', 'status', 'proposal',  'proposal_author', 'initiator',  'initial_message')
        }),
        ('Notifications', {
            'fields': ('proposal_author_notification_type', 'initiator_notification_type',)
        }),
        ('Dates', {
            'fields': ('last_message', 'created',)
        }),
    )
    inlines = [MessgesInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'created']
    fields = ('id', 'author', 'is_unread', 'chatroom', 'content', 'created')
