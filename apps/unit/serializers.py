from rest_framework import serializers

from .models import Unit, Address
from apps.filter.models import City, CityArea, Service


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class CityAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityArea
        exclude = ("city",)


class AddressSerializer(serializers.ModelSerializer):
    city = CitySerializer()
    city_area = CityAreaSerializer()

    class Meta:
        model = Address
        fields = "__all__"


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"


class UnitSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    services = ServiceSerializer(many=True)

    class Meta:
        model = Unit
        fields = "__all__"
