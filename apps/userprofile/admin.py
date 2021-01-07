from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Profile

# from django.contrib.auth.admin import UserAdmin, GroupAdmin
# from django.contrib.auth.models import User, Group
# from django.contrib.auth.models import Group
# admin.site.unregister(User)
# admin.site.unregister(Group)
# admin.site.register(User)
# admin.site.register(Group)
# admin.site.register(Profile)


@admin.register(Profile)
class ProfileAdmin(UserAdmin):
    """Inherit from UserAdmin for hashing password during creatint new user"""
    readonly_fields = ['avatar_thumb', 'last_login', 'date_joined']

    def avatar_thumb(self, obj):
        return format_html('<img src="{url}" width="200px" height="auto" />'.format(
            url=obj.avatar.url,
            width=obj.avatar.width,
            height=obj.avatar.height,
        ))
