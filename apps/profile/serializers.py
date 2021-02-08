from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """
    SerializerMethodField call get_<filed_name> for creatin this field
    """
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'avatar', 'username', 'email', 'first_name', 'birth_year', 'sex',
                  'last_name', 'description']

    def get_avatar(self, obj):
        request = self.context.get('request')

        if obj.avatar:
            return request.build_absolute_uri(obj.avatar.url)

        return ''
