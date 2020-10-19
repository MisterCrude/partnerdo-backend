from rest_framework import serializers

from .models import City, CityArea


class CitySerializer(serializers.ModelSerializer):
    areas = serializers.SerializerMethodField('get_related_areas')

    def get_related_areas(self, object):
        related_areas = CityArea.objects.filter(
            city__id=object.id).values('id', 'name')
        return related_areas

    class Meta:
        model = City
        fields = ('id', 'name', 'areas')
