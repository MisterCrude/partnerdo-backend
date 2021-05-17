import datetime
import uuid

from core.consts import GENDER_CHOICES
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group as BaseGroup
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext as _


def current_year():
    return datetime.datetime.now().year


class ProfileAvatar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    image = models.ImageField(
        upload_to='uploads/userprofile/', max_length=100)

    def __str__(self):
        if hasattr(self, 'user'):
            return f'{self.user.username}'
        else:
            return _('- not assigned -')

    def delete(self, *args, **kwargs):
        user = User.objects.filter(avatar__id=self.id)
        user.update(avatar='')
        self.image.delete()
        super(ProfileAvatar, self).delete(*args, **kwargs)


class User(AbstractUser):
    """
    Set name for custom user model ad 'User' otherwise it involve "auth_group" db error
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    # use models.DO_NOTHING for ability unpin avatar for chosen profile
    avatar = models.OneToOneField(
        ProfileAvatar, on_delete=models.SET_NULL, null=True, blank=True)
    # TODO null=True for creating superuser by shell, because I can't provide this field in shell, need to refactor
    birth_year = models.IntegerField(null=True, validators=[MinValueValidator(
        current_year() - 100), MaxValueValidator(current_year())])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    description = models.TextField(max_length=200)

    def delete(self, *args, **kwargs):
        if self.avatar:
            ProfileAvatar.objects.get(pk=self.avatar.id).delete()
        super(User, self).delete(*args, **kwargs)


class Group(BaseGroup):
    """
    This model needed for merge custom User model and Base Group in one section in admin
    """
    class Meta:
        proxy = True
