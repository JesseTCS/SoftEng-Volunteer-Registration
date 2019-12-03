from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime


# Create your models here.

class Address(models.Model):
    address1 = models.CharField(
        "Address line 1",
        max_length=1024,
    )

    address2 = models.CharField(
        "Address line 2",
        max_length=1024,
    )

    zip_code = models.CharField(
        "ZIP / Postal code",
        max_length=12,
    )

    city = models.CharField(
        "City",
        max_length=1024,
    )

    country = models.CharField(
        "Country",
        max_length=3,
    )
class TimeSlot(models.Model):
    Event_Name = models.CharField(max_length=100, default='Event')
    ACTIVITY_CHOICES = (
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
        )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    address = models.ForeignKey(Address,null=True,on_delete=models.SET_NULL)
    activity_level = models.CharField(max_length=1, choices=ACTIVITY_CHOICES, blank=True)
    description = models.TextField(blank=True)
    num_signed_up = models.IntegerField(default=0)
    num_needed = models.IntegerField()
    volunteer = models.ManyToManyField(User)
    
    def __str__(self):
        return self.Event_Name