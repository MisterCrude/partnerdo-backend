from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views


API_PREFIX = 'api/v1.0'

urlpatterns = [
    path(route=r'admin/',
         view=admin.site.urls),

    path(route=f'{API_PREFIX}/units/',
         view=include('apps.unit.urls')),

    path(route=f'{API_PREFIX}/filters/',
         view=include('apps.filter.urls')),

    path(route=f'{API_PREFIX}/token/',
         view=jwt_views.TokenObtainPairView.as_view(),
         name='obtain-token-pair'),

    path(route=f'{API_PREFIX}/token-refresh/',
         view=jwt_views.TokenRefreshView.as_view(),
         name='token-refresh'),

    path(route=f'{API_PREFIX}/register/',
         view=include('apps.user.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
