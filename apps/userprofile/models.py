import uuid
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    avatar = models.ImageField(
        upload_to='uploads/userprofile/', max_length=100, blank=True)
    description = models.TextField(max_length=200, blank=True)
    short_description = models.TextField(max_length=100, blank=True)
