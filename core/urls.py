from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

API_PREFIX = 'api/v1.0'

urlpatterns = [
    path(route=r'admingus/',
         view=admin.site.urls),

    path(route=f'{API_PREFIX}/proposals/',
         view=include('apps.proposal.urls')),

    path(route=f'{API_PREFIX}/auth/',
         view=include('dj_rest_auth.urls')),

    #     path(route=f'{API_PREFIX}/auth/registration/',
    #          view=include('dj_rest_auth.registration.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
