from core.utils import get_usersettings_model
from rest_framework import serializers
from django.http import QueryDict
import datetime

from apps.proposal.models import Proposal, City, CityArea, Category


##
# Filters
##


class CityAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityArea
        fields = ('id', 'name')


class CitySerializer(serializers.ModelSerializer):
    city_areas = CityAreaSerializer(many=True)

    class Meta:
        model = City
        fields = ('id', 'name', 'city_areas')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


##
# Proposal
##

class AuthorSerializer(serializers.ModelSerializer):
    """
    SerializerMethodField call get_<filed_name> for creatin this field
    """
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = get_usersettings_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'avatar')

    def get_avatar(self, obj):
        request = self.context.get('request')

        if obj.avatar:
            return request.build_absolute_uri(obj.avatar.url)

        return ''


class ProposalCitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name')


class ProposalSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    category = CategorySerializer()
    city = ProposalCitySerializer()
    city_area = CityAreaSerializer()

    class Meta:
        model = Proposal
        fields = '__all__'
