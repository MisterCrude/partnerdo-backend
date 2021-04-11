from rest_framework import serializers

from .models import User, ProfileAvatar
from apps.proposal.serializers import ProposalSerializer
from apps.proposal.models import Proposal

##
# Profile
# your profile data
##


class ProfileSerializer(serializers.ModelSerializer):
    """
    SerializerMethodField call get_<filed_name> for creatin this field
    """
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField(read_only=True)
    avatar = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'avatar', 'username', 'email', 'first_name', 'birth_year', 'gender',
                  'last_name', 'description')

    # TODO use util here
    def get_avatar(self, obj):
        if obj.avatar is not None:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.avatar.image.url)

        return ''


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'avatar', 'username', 'email', 'first_name', 'birth_year', 'gender',
                  'last_name', 'description')


class CreateProfileAvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileAvatar
        fields = '__all__'


class RetrieveProfileAvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ProfileAvatar
        fields = '__all__'

    # TODO use util here
    def get_avatar(self, obj):
        request = self.context.get('request')

        if obj.avatar:
            return request.build_absolute_uri(obj.avatar.image.url)

        return ''


##
# User
# proposal data for exact user
##
class UserProposalsSerializer(ProposalSerializer):
    author = None

    class Meta:
        model = Proposal
        exclude = ('author',)


class UserSerializer(serializers.ModelSerializer):
    proposals = UserProposalsSerializer(many=True)
    avatar = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'avatar', 'username', 'email',
                  'first_name', 'last_name', 'description', 'proposals')

    # TODO use util here
    def get_avatar(self, obj):
        request = self.context.get('request')

        if obj.avatar:
            return request.build_absolute_uri(obj.avatar.image.url)

        return ''
