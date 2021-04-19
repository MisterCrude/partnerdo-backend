from django.urls import path

from .views import ProfileRetrieveAPIView, ProfileAvatarCreateAPIView


"""
Retrive data some user by ID
"""
urlpatterns = [
    path(route=r'avatar',
         view=ProfileAvatarCreateAPIView.as_view(),
         name='create_profile_avatar'),

    path(route=r'<uuid:pk>',  # GET item
         view=ProfileRetrieveAPIView.as_view(),
         name='profile'),
]
