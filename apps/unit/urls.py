from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'', views.UnitViewSet)

urlpatterns = [
    path(route=r'',
         view=include(router.urls),
         name="units"),
]
