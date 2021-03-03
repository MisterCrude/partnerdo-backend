import datetime
import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group as BaseGroup
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext as _


SEX_CHOICES = [
    ('m', 'male'),
    ('f', 'female')
]


def current_year():
    return datetime.datetime.now().year


class User(AbstractUser):
    """
    Set name for custom user model ad 'User' otherwise it involve "auth_group" db error
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    avatar = models.ImageField(
        upload_to='uploads/userprofile/', max_length=100, blank=True)
    birth_year = models.IntegerField(validators=[MinValueValidator(
        current_year() - 100), MaxValueValidator(current_year())], blank=True, null=True)
    gender = models.CharField(
        max_length=1, choices=SEX_CHOICES, default=SEX_CHOICES[0][0])
    description = models.TextField(max_length=200)


class Group(BaseGroup):
    """
    This model needed for merge custom User model and Base Group in one section in admin
    """
    class Meta:
        proxy = True
