from django.apps import apps
from django.contrib import admin
from django.contrib.auth import models
from django.contrib.auth.admin import UserAdmin

from .models import Profile

""" Move default user Group model to custom app section in admin """
apps.get_model('auth.Group')._meta.app_label = 'userprofile'


@admin.register(Profile)
class ProfileAdmin(UserAdmin):
    """ Inherit from UserAdmin for hashing password during creatint new user """
    readonly_fields = ['avatar_thumb', 'last_login', 'date_joined']

    def avatar_thumb(self, obj):
        return format_html('<img src="{url}" width="200px" height="auto" />'.format(
            url=obj.avatar.url,
            width=obj.avatar.width,
            height=obj.avatar.height,
        ))
