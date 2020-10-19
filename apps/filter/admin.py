from django.contrib import admin
from .models import CityArea, City


class CityAreaInline(admin.TabularInline):
    readonly_fields = ["id"]
    model = CityArea
    extra = 0


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]
    inlines = [CityAreaInline]


@admin.register(CityArea)
class CityAreaAdmin(admin.ModelAdmin):
    readonly_fields = ["id"]
