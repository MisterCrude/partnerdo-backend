from rest_framework import serializers

from apps.proposal.models import Proposal


class ProposalSerializer(serializers.ModelSerializer):
    # city = serializers.CharField(source='city.name', read_only=True)
    # city_area = serializers.CharField(source='city_area.name', read_only=True)

    def to_representation(self, instance):
        rep = super(ProposalSerializer, self).to_representation(instance)
        rep['city'] = instance.city.name
        rep['city_area'] = instance.city_area.name
        return rep

    class Meta:
        model = Proposal
        # fields = '__all__'
        fields = ('id', 'name', 'description', 'city', 'city_area')
