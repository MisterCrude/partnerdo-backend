from django.urls import path

from .views import (ChatroomChangeStatusAPIView, ChatroomCreateAPIView,
                    ChatroomDetailsAPIView, ChatroomListAPIView)

urlpatterns = [

    path(route=r'',  # GET list
         view=ChatroomListAPIView.as_view(),
         name='proposal_chatrooms'),

    path(route=r'<uuid:pk>',
         view=ChatroomDetailsAPIView.as_view(),
         name='proposal_chatroom_detailse'),

    path(route=r'create',
         view=ChatroomCreateAPIView.as_view(),
         name='proposal_chatroom_create'),

    path(route=r'<uuid:pk>/<str:status>',
         view=ChatroomChangeStatusAPIView.as_view(),
         name='proposal_chatroom_update_status'),
]
