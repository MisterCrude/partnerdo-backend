from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from .views import FacebookLoginView


API_PREFIX = 'api/v1.0'

urlpatterns = [
    path(route=r'admingus/',
         view=admin.site.urls),

    path(route=f'{API_PREFIX}/auth/',
         view=include('dj_rest_auth.urls')),

    path(route=f'{API_PREFIX}/auth/registration/',
         view=include('dj_rest_auth.registration.urls')),

    path(route=f'{API_PREFIX}/auth/facebook/',
         view=FacebookLoginView.as_view(),
         name='facebook-login')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
