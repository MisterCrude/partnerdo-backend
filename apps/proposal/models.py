import uuid
from django.db import models
from django.utils.text import slugify


class CityArea(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    city = models.ForeignKey(
        'City', related_name='city_areas', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'Areas'


class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Cities'


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
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
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('slug', 'parent',)
        verbose_name_plural = "categories"


class Proposal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    city = models.ForeignKey(
        'City', related_name='proposals', on_delete=models.SET_NULL, null=True)
    city_area = models.ForeignKey(
        'CityArea', related_name='proposals', on_delete=models.SET_NULL, null=True)
    location_note = models.CharField(max_length=100, blank=True)
    image = models.ImageField(
        upload_to='uploads/', max_length=100, blank=True)
    category = models.ForeignKey(
        'Category',  on_delete=models.SET_NULL, null=True, blank=True)
    author = models.ForeignKey(
        'auth.User', on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_cat_list(self):
        k = self.category
        breadcrumb = ["dummy"]

        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent

        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])

        return breadcrumb[-1:0:-1]

    class Meta:
        verbose_name_plural = 'Proposals'
