from rest_framework import serializers

from apps.proposal.models import Proposal
from apps.proposal.serializers import ProposalSerializer

from .models import ProfileAvatar, User

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

    def get_avatar(self, obj):
        if obj.avatar is not None:
            return obj.avatar.image.url

        return ''


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'avatar', 'username', 'email', 'first_name', 'birth_year', 'gender',
                  'last_name', 'description')


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileAvatar
        fields = '__all__'


##
# User
# proposal data for some user
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

    def get_avatar(self, obj):
        if obj.avatar:
            return obj.avatar.image.url

        return ''
