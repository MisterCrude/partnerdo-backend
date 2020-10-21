from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView


class FacebookLoginView(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    # callback_url = 'localhost:8000'
