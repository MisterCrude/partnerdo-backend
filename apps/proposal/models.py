import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

PROPOSAL_RESPONSE_STATUS = [
    (0, _('Idle')),
    (1, _('Approved')),
    (2, _('Rejected')),
]


class CityArea(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=30)
    city = models.ForeignKey(
        'City', related_name='city_areas', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Area'
        verbose_name_plural = 'City areas'


class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Cities'


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=30)
    color = models.CharField(max_length=7, default='#dd6b21')
    image = models.ImageField(
        upload_to='uploads/categories/', max_length=100, blank=True)
    # TODO uncommit it when will working on subcategories
    # parent = models.ForeignKey(
    #     'self', on_delete=models.CASCADE, related_name='categories', null=True, blank=True)

    def __str__(self):
        return self.name
        # full_path = [self.name]

        # if self.parent:
        #     k = self.parent
        #     while k is not None:
        #         full_path.append(k.name)
        #         k = k.parent

        # return ' > '.join(full_path[::-1])

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Category, self).delete(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'


class Proposal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='proposals', on_delete=models.PROTECT)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)
    city = models.ForeignKey(
        'City', related_name='proposals', on_delete=models.PROTECT)
    city_area = models.ForeignKey(
        'CityArea', related_name='proposals', on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(max_length=800)
    title = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Proposals'
