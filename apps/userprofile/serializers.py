from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'avatar', 'username', 'email', 'first_name',
                  'last_name', 'description', 'short_description']
        # fields = "__all__"

    def get_avatar(self, obj):
        print("test", obj.avatar)

        if obj.avatar:
            return obj.avatar

        return 'https://static.productionready.io/images/smiley-cyrus.jpg'
