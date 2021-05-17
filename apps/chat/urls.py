from django.urls import path

from .views import (ChatRoomChangeStatusAPIView, ChatRoomCreateAPIView,
                    ChatRoomDetailsAPIView, ChatRoomListAPIView)

urlpatterns = [

    path(route=r'',  # GET list
         view=ChatRoomListAPIView.as_view(),
         name='proposal_chat_rooms'),

    path(route=r'<uuid:pk>',
         view=ChatRoomDetailsAPIView.as_view(),
         name='proposal_chat_room_detailse'),

    path(route=r'create',
         view=ChatRoomCreateAPIView.as_view(),
         name='proposal_chat_room_create'),

    path(route=r'<uuid:pk>/<str:status>',
         view=ChatRoomChangeStatusAPIView.as_view(),
         name='proposal_chat_room_update_status'),
]
