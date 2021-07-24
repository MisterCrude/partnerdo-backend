from core.utils import create_admin_thumb
from django.contrib import admin
from django.contrib.auth.admin import Group as BaseGroup
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Group, ProfileAvatar, User


def replace_fields_for_useradmin(admin_fields, new_fields):
    fields = list(admin_fields)

    del fields[1]
    fields.insert(1, new_fields)

    return tuple(fields)


"""
Hide defalut Group from admin
"""
admin.site.unregister(BaseGroup)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Inherit from UserAdmin for hashing password during creatint new user
    """

    fieldsets = replace_fields_for_useradmin(BaseUserAdmin.fieldsets, (_('Personal info'), {'fields': (
        'id', 'first_name', 'last_name', 'email', 'channel_name', (
            'avatar', 'avatar_thumb'),
        'birth_year', 'gender', 'description')}))

    readonly_fields = ['id', 'channel_name',
                       'avatar_thumb', 'last_login', 'date_joined']

    def avatar_thumb(self, obj):
        return create_admin_thumb(obj.avatar.image if obj.avatar else None)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    pass


@admin.register(ProfileAvatar)
class ProfileAvatarAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'image_thumb')
    fieldsets = (
        (None, {
            'fields': ('id', ('image', 'image_thumb'))
        }),
    )

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.delete()

    def image_thumb(self, obj):
        return create_admin_thumb(obj.image)
