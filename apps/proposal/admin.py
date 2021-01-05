import os
from django import forms
from django.contrib import admin
from django.conf import settings
from django.utils.safestring import mark_safe

from .models import Proposal, City, CityArea, Category


##
# City
##

class CityAreaInline(admin.TabularInline):
    readonly_fields = ['id']
    model = CityArea
    extra = 0


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    fields = ('id', 'name')
    inlines = [CityAreaInline]


##
# CityArea
##

@admin.register(CityArea)
class CityAreaAdmin(admin.ModelAdmin):
    readonly_fields = ['id']


##
# Proposal
##

class CityAreaChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.city} > {obj.name}'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'image_thumb', 'created', 'updated']
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'category', 'author')
        }),
        (None, {
            'fields': ('image', 'image_thumb'),
        }),
        ('Location', {
            'fields': ('city', 'city_area', 'location_note'),
        }),
        ('Dates', {
            'fields': ('updated', 'created'),
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'city_area':
            return CityAreaChoiceField(queryset=CityArea.objects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def image_thumb(self, obj):
        thumb_path = f'{settings.BASE_DIR}{obj.image.url}'

        if (os.path.exists(thumb_path)):
            render_thumb = f'<span style="width: 170px; height: 170px; display: block;"><img style="max-width: 100%; max-height: 100%;" src="{obj.image.url}" width="{obj.image.width}" height={obj.image.height} /></span>'

            return mark_safe(render_thumb)
        else:
            return "Can't find image"
