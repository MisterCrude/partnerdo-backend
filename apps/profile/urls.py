from django.urls import path

from .views import UserRetrieveAPIView


"""
Retrive data some user by ID
"""
urlpatterns = [
    path(route=r'<uuid:pk>',  # GET item
         view=UserRetrieveAPIView.as_view(),
         name='user'),
]
