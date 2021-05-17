from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token


@database_sync_to_async
def get_user(token_str):
    return Token.objects.get(key=token_str).user


class TokenAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        query_params_list = scope['query_string'].decode().split('&')
        query_params_dict = dict(param.split('=')
                                 for param in query_params_list)

        if 'token' in query_params_dict:
            try:
                token_str = query_params_dict.get('token')
                user = await get_user(token_str)
                scope['user'] = user
            except Token.DoesNotExist:
                scope['user'] = AnonymousUser()

        return await self.inner(scope, receive, send)


def TokenAuthMiddlewareStack(inner): return TokenAuthMiddleware(
    AuthMiddlewareStack(inner))
