import os
from django.contrib import admin
from django.conf import settings
from django.utils.safestring import mark_safe

from .models import Proposal, City, CityArea, Category


class CityAreaInline(admin.TabularInline):
    readonly_fields = ["id"]
    model = CityArea
    extra = 0


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]
    fields = ("id", "name")
    inlines = [CityAreaInline]

    def property_value(self, obj):
        return obj.get_value()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # readonly_fields = ["slug"]
    pass


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    readonly_fields = ["id", "image_thumb", "created", "updated"]
    fieldsets = (
        (None, {
            "fields": ("name", "description", "author")
        }),
        (None, {
            "fields": ("image", "image_thumb"),
        }),
        ("Location", {
            "fields": ("city", "city_area", "location_note"),
        }),
        ("Dates", {
            "fields": ("updated", "created"),
        }),
    )

    def image_thumb(self, obj):
        thumb_path = f'{settings.BASE_DIR}{obj.logo.url}'

        if (os.path.exists(thumb_path)):
            render_thumb = f'<span style="width: 170px; height: 170px; display: block;"><img style="max-width: 100%; max-height: 100%;" src="{obj.logo.url}" width="{obj.logo.width}" height={obj.logo.height} /></span>'

            return mark_safe(render_thumb)
        else:
            return "Can't find image"
