from rest_framework import serializers

from apps.proposal.models import Proposal, City, CityArea, Category


##
# Proposal
##


class ProposalSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        rep = super(ProposalSerializer, self).to_representation(instance)
        rep['city'] = instance.city.name
        rep['city_area'] = instance.city_area.name

        return rep

    class Meta:
        model = Proposal
        # fields = '__all__'
        fields = ('id', 'name', 'description',
                  'city', 'city_area', 'image')


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
        model = CityArea
        fields = ('id', 'name')
