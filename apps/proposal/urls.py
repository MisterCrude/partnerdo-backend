from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import FiltersView, ProposalListAPIView, ProposalDetailsAPIView, ProposalCreateUpdateAPIView

# router = DefaultRouter()
# router.register(r'', views.ProposalViewSet, basename='proposal')

urlpatterns = [
    path(route=r'',  # GET list
         view=ProposalListAPIView.as_view(),
         name='proposals'),

    path(route=r'create',  # POST, PATCH
         view=ProposalCreateUpdateAPIView.as_view(),
         name='create_proposal'),

    path(route=r'<uuid:pk>',  # GET item, DELETE
         view=ProposalDetailsAPIView.as_view(),
         name='proposal'),

    path(route=r'filters',
         view=FiltersView.as_view(),
         name='filters'),
]
