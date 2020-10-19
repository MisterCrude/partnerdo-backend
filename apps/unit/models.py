import uuid
from django.db import models


class Phone(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    phone_number = models.CharField(max_length=60)
    address = models.ForeignKey(
        "address", related_name='phones', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = 'Phone'
        verbose_name_plural = 'Phones'


class Email(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email_address = models.EmailField()
    address = models.ForeignKey(
        "address", related_name='emails', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.email_address

    class Meta:
        verbose_name = 'Email'
        verbose_name_plural = 'Emails'


class Address(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    zipcode = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    building = models.PositiveSmallIntegerField()
    room = models.PositiveSmallIntegerField(blank=True, null=True)
    site = models.CharField(max_length=100, blank=True)
    city = models.ForeignKey(
        "filter.City", related_name='addresses', on_delete=models.SET_NULL, null=True)
    city_area = models.ForeignKey(
        "filter.CityArea", related_name='addresses', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.city}, {self.street} {self.building}"

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'


class Unit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=60, blank=True)
    logo = models.ImageField(
        upload_to='uploads/', max_length=100)
    services = models.ManyToManyField("filter.Service")
    address = models.ForeignKey(
        "Address", related_name='units', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Unit'
        verbose_name_plural = 'Units'
