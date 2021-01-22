import uuid
from django.conf import settings
from django.db import models


class CityArea(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    city = models.ForeignKey(
        'City', related_name='city_areas', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'City areas'


class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Cities'


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL,  related_name='children', blank=True, null=True,)

    def __str__(self):
        full_path = [self.name]
        k = self.parent

        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path[::-1])

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'


class Proposal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        'Category',  on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(
        'City', related_name='proposals', on_delete=models.SET_NULL, null=True)
    city_area = models.ForeignKey(
        'CityArea', related_name='proposals', on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=800)
    image = models.ImageField(
        upload_to='uploads/proposal/', max_length=100, blank=True)
    location_note = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Proposals'
