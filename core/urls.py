from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.permissions import AllowAny
from rest_framework.schemas import get_schema_view

API_PREFIX = 'api/v1.0'

urlpatterns = [
    path(route=r'admingus/',
         view=admin.site.urls),

    path(route=f'{API_PREFIX}/proposals/',
         view=include('apps.proposal.urls')),

    path(route=f'{API_PREFIX}/user/',
         view=include('apps.profile.urls')),

    path(route=f'{API_PREFIX}/chat-rooms/',
         view=include('apps.chat.urls')),

    path(route=f'{API_PREFIX}/auth/',
         view=include('dj_rest_auth.urls')),

    path(route=f'{API_PREFIX}/auth/registration/',
         view=include('dj_rest_auth.registration.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    """
    Generate API dynamic documentation
    """
    urlpatterns += path(f'{API_PREFIX}/openapi', get_schema_view(
        title="PartnerDo API",
        version=API_PREFIX,
        permission_classes=[
            AllowAny]
    ), name='openapi-schema'),
