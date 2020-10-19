import os
from django.conf import settings
from django.contrib import admin
from django.utils.safestring import mark_safe


from .models import Unit, Address, Phone, Email


class EmailInline(admin.TabularInline):
    readonly_fields = ["id"]
    model = Email
    extra = 0


class PhoneInline(admin.TabularInline):
    readonly_fields = ["id"]
    model = Phone
    extra = 0


@admin.register(Address)
class CityAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]
    inlines = [PhoneInline, EmailInline]


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    readonly_fields = ["id", 'logo_thumb']
    fieldsets = (
        ('', {
            'fields': ('name', 'description', ("logo", "logo_thumb"), "services", "address", "id"),
        }),
    )

    def logo_thumb(self, obj):
        thumb_path = f'{settings.BASE_DIR}{obj.logo.url}'

        if (os.path.exists(thumb_path)):
            render_thumb = f'<span style="width: 170px; height: 170px; display: block;"><img style="max-width: 100%; max-height: 100%;" src="{obj.logo.url}" width="{obj.logo.width}" height={obj.logo.height} /></span>'

            return mark_safe(render_thumb)
        else:
            return "Can't find image"


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]
