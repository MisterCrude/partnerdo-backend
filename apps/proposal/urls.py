from rest_framework.routers import DefaultRouter
from django.urls import path, include

from . import views

router = DefaultRouter()
router.register(r'', views.ProposalViewSet)

urlpatterns = [
    path(route=r'',
         view=include(router.urls),
         name='proposals'),

    path(route=r'filters',
         view=views.FiltersView.as_view(),
         name='filters'),
]
