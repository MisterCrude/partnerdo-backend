from django.urls import path

from .views import UserRetrieveAPIView, ProfileAvatarCreateAPIView


"""
Retrive data some user by ID
"""
urlpatterns = [
    path(route=r'avatar',
         view=ProfileAvatarCreateAPIView.as_view(),
         name='create_user_avatar'),

    path(route=r'<uuid:pk>',  # GET item
         view=UserRetrieveAPIView.as_view(),
         name='user'),
]
