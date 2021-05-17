from django.urls import path

from .views import (FiltersAPIView, ProposalCreateAPIView,
                    ProposalDetailsAPIView, ProposalListAPIView)

urlpatterns = [
    path(route=r'',  # GET list
         view=ProposalListAPIView.as_view(),
         name='proposals'),

    path(route=r'create',  # POST,
         view=ProposalCreateAPIView.as_view(),
         name='create_proposal'),

    path(route=r'<uuid:pk>',  # GET item, DELETE, PATCH
         view=ProposalDetailsAPIView.as_view(),
         name='proposal'),

    path(route=r'filters',
         view=FiltersAPIView.as_view(),
         name='filters'),
]
