from rest_framework import serializers

from .models import City, Service, CityArea


class CitySerializer(serializers.ModelSerializer):
    areas = serializers.SerializerMethodField('get_related_areas')

    def get_related_areas(self, object):
        related_areas = CityArea.objects.filter(
            city__id=object.id).values('id', 'name')
        return related_areas

    class Meta:
        model = City
        fields = ('id', 'name', 'areas')


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
