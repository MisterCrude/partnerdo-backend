from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.chat'

    def ready(self):
        from . import receivers  # noqa: F401 // ignore flake8 error
