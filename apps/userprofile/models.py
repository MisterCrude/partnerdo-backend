import datetime
import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


SEX_CHOICES = [
    ('m', 'male'),
    ('f', 'female')
]


def current_year():
    return datetime.datetime.now().year


class Profile(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    avatar = models.ImageField(
        upload_to='uploads/userprofile/', max_length=100, blank=True)
    birth_year = models.IntegerField(validators=[MinValueValidator(
        current_year() - 100), MaxValueValidator(current_year())], null=True)
    sex = models.CharField(
        max_length=1, choices=SEX_CHOICES, default=SEX_CHOICES[0][0])
    description = models.TextField(max_length=200, blank=True)
    short_description = models.TextField(max_length=100, blank=True)

    """
    db_table = 'auth_user' must added for custom user based on AbstractUser
    for avoid auth_group migration error
    """
    class Meta:
        db_table = 'auth_user'
