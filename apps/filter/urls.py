from django.urls import path

from . import views


urlpatterns = [
    path(route=r'',
         view=views.FilterAPIView.as_view(),
         name="filters"),
]
