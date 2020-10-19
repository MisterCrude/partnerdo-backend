from django.urls import path

from . import views

urlpatterns = [
    path(route=r'',
         view=views.RegistrationAPIView.as_view(),
         name='register')
]
