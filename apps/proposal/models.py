import uuid
from django.db import models


class Proposal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=60, blank=True)
    image = models.ImageField(
        upload_to='uploads/', max_length=100)
    # address = models.ForeignKey(
    #     "Address", related_name='units', on_delete=models.SET_NULL, null=True)
    author = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'proposal'
        verbose_name_plural = 'proposals'
