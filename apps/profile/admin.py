from django.apps import apps
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from core.utils import create_thumb

from .models import User


def replace_fields_for_useradmin(admin_fields, new_fields):
    fields = list(admin_fields)

    del fields[1]
    fields.insert(1, new_fields)

    return tuple(fields)


""" 
Move default user Group model to custom app section in admin 
"""
# apps.get_model('auth.Group')._meta.app_label = 'profile'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """    
    Inherit from UserAdmin for hashing password during creatint new user 
    """

    fieldsets = replace_fields_for_useradmin(BaseUserAdmin.fieldsets, (_('Personal info'), {'fields': (
        'first_name', 'last_name', 'email', ('avatar', 'avatar_thumb'),
        'birth_year', 'sex', 'short_description', 'description')}))

    readonly_fields = ['avatar_thumb', 'last_login', 'date_joined']

    def avatar_thumb(self, obj):
        return create_thumb(obj.avatar)
