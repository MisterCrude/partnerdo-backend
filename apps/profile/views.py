from django.shortcuts import render
from django.utils.translation import gettext as _
from rest_framework.exceptions import ParseError
from rest_framework.generics import RetrieveAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_201_CREATED, HTTP_200_OK
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer, CreateProfileAvatarSerializer
from .models import User, ProfileAvatar, User


class ProfileRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileAvatarCreateAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def delete(self, request):
        profile = User.objects.filter(pk=request.user.id)

        profile_avatar = [item for item in profile.values('avatar')][0]
        profile_avatar_id = profile_avatar.get('avatar')

        if not profile_avatar_id:
            return Response(status=HTTP_200_OK)
        else:
            try:
                ProfileAvatar.objects.get(pk=profile_avatar_id).delete()
            except:
                raise ParseError(_("Can't delete avatar"),
                                 code='can_not_delete_avatar')

        return Response(status=HTTP_200_OK)

    def post(self, request):
        profile = User.objects.filter(pk=request.user.id)

        """
        Check if image field exists in request body and save as model instance
        """
        if request.data.get('image'):
            # Delete existing avatar if present
            profile_avatar = [
                item for item in profile.values('avatar')][0]
            profile_avatar_id = profile_avatar.get('avatar')

            if profile_avatar_id:
                ProfileAvatar.objects.get(
                    pk=profile_avatar_id).delete()

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
        Update avatar in existing model instance
        """
        try:
            profile.update(avatar=profile_avatar)

        except:
            raise ParseError(_("Can't update avatar field in profile"),
                             code='can_not_update_or_create_image')

        return Response(request_serilaizer.data.get('image'), status=HTTP_201_CREATED)
