from django.shortcuts import render
from django.utils.translation import gettext as _
from rest_framework.exceptions import ParseError
from rest_framework.generics import RetrieveAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, CreateProfileAvatarSerializer, RetrieveProfileAvatarSerializer, UpdateProfileSerializer
from .models import User, ProfileAvatar


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileAvatarCreateAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        """
        Check if profile_id field exists in request body and check if exists user with this id
        """
        try:
            profile_id = request.data['profile_id']
            profile = User.objects.filter(pk=profile_id)

        except:
            raise ParseError(_("Can't find profile with provided profile_id"),
                             code='profile_does_not_exist')

        """
        Check if image field exists in request body and save as model instance
        """
        if request.data.get('image'):
            request_serilaizer = CreateProfileAvatarSerializer(
                data=request.data)
            request_serilaizer.is_valid(raise_exception=True)
            request_serilaizer.save()

            profile_avatar = ProfileAvatar.objects.get(
                pk=request_serilaizer.data.get('id'))

        else:
            raise ParseError(_("Request hasn't avatar file attached"),
                             code='image_file_not_attached')

        """
        Check if profile_id field exists in request body and check if exists user with this id
        """
        try:
            profile.update(avatar=profile_avatar)

        except:
            raise ParseError(_("Can't update avatar field in profile"),
                             code='can_not_update_or_create_image')

        return Response(request_serilaizer.data.get('image'), status=HTTP_201_CREATED)
