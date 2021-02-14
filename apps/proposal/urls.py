from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import ProposalAPIView
from .views import ProposalProposalAPIViewDetails

# router = DefaultRouter()
# router.register(r'', views.ProposalViewSet, basename='proposal')

urlpatterns = [
    path(route=r'',
         view=ProposalAPIView.as_view(),
         name='proposals'),

    path(route=r'<uuid:pk>',
         view=ProposalProposalAPIViewDetails.as_view(),
         name='proposal'),

    # path(route=r'',
    #      view=include(router.urls),
    #      name='proposals'),

    # path(route=r'filters',
    #      view=views.FiltersView.as_view(),
    #      name='filters'),
]
