from core.utils import create_thumb
from django import forms
from django.contrib import admin

from .models import Category, City, CityArea, Proposal

##
# City
##


class CityAreaInline(admin.TabularInline):
    readonly_fields = ('id',)
    model = CityArea
    extra = 0


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fields = ('id', 'name')
    inlines = [CityAreaInline]


##
# CityArea
##

@admin.register(CityArea)
class CityAreaAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


##
# Proposal
##

class CityAreaChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.city} > {obj.name}'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'image_thumb']
    fieldsets = (
        (None, {
            'fields': ('id', 'name', ('image', 'image_thumb'), 'color')
        }),
    )

    def image_thumb(self, obj):
        return create_thumb(obj.image)

    def delete_queryset(self, queryset):
        for obj in queryset:
            obj.delete()


@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'created', 'updated']
    fieldsets = (
        (None, {
            'fields': ('id', 'title', 'description', 'category', 'author')
        }),
        ('Location', {
            'fields': ('city', 'city_area'),
        }),
        ('Dates', {
            'fields': ('updated', 'created'),
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'city_area':
            return CityAreaChoiceField(queryset=CityArea.objects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
