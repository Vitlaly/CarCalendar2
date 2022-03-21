from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


class Owner(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    car = models.CharField(max_length=200, null=True)
    mileage = models.FloatField(null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Component(models.Model):
    STATUS = (
        ('winter', 'winter'),
        ('all season', 'all season'),
        ('summer', 'summer'),
    )
    measurement = (
        ('Km', 'km'),
        ('Months', 'months'),
    )
    name = models.CharField(max_length=200, null=True)
    resource = models.FloatField(null=True, blank=True)
    unit = models.CharField(max_length=200, null=True, choices=measurement)
    description = models.CharField(max_length=600, null=True, blank=True)
    mileage_installation = models.FloatField(null=True, blank=True)
    date_installation = models.DateTimeField(null=True, blank=True, default=datetime.datetime.now())
    owner = models.ForeignKey(Owner, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200, null=True, choices=STATUS, default='all season')

    def __str__(self):
        return self.name






