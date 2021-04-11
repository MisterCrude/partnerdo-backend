from django.conf import settings
from django.utils.safestring import mark_safe


def create_thumb(avatar):
    if (avatar.image):
        thumb_path = avatar.image.url
        render_thumb = f'<span style="width: 170px; height: 170px; display: block;"><img style="max-width: 100%; max-height: 100%;" src="{thumb_path}" width="100px" height="auto" /></span>'

        return mark_safe(render_thumb)
    else:
        return "-"


def get_usersettings_model():
    """
    Returns the ``UserSettings`` model that is active in this project.
    """
    try:
        from django.apps import apps
        get_model = apps.get_model
    except ImportError:
        from django.db.models.loading import get_model

    try:
        app_label, model_name = settings.AUTH_USER_MODEL.split('.')
    except ValueError:
        raise ImproperlyConfigured('USERSETTINGS_MODEL must be of the '
                                   'form "app_label.model_name"')
    usersettings_model = get_model(app_label, model_name)

    if usersettings_model is None:
        raise ImproperlyConfigured('AUTH_USER_MODEL refers to model "%s" that has '
                                   'not been installed' % settings.AUTH_USER_MODEL)
    return usersettings_model
