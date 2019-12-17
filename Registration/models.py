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
        null = True
    )

    zip_code = models.CharField(
        "ZIP / Postal code",
        max_length=12,
    )

    city = models.CharField(
        "City",
        max_length=1024,
    )

    state = models.CharField(
        "State",
        max_length=1024,
        null = True
    )

    country = models.CharField(
        "Country",
        max_length=3,
    )

    def __str__(self):
        return self.address1 + ' ' + self.city + ' ' + self.state + ' ' + self.zip_code

class PhoneNumber(models.Model):
    area_code = models.CharField(max_length=3)
    numbers1 = models.CharField(max_length=3)
    numbers2 = models.CharField(max_length=4)

    def __str__(self):
        return str(self.area_code) + '-' + str(self.numbers1) + '-' + str(self.numbers2)

class CustomUser(models.Model):
    user_account = models.ForeignKey(User, related_name='user', null=True, on_delete=models.SET_NULL)
    phone_number = models.ManyToManyField(PhoneNumber, related_name='phone_number')
    birthday = models.DateField(null=True)
    def __str__(self):
        return self.user_account.username

class Business(models.Model):
    business_name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)
    corporate_users = models.ManyToManyField(CustomUser)
    opt_in = models.ManyToManyField(CustomUser, related_name='opt_in')
    phone_number = models.ManyToManyField(PhoneNumber)
    
    def __str__(self):
        return self.business_name
class TimeSlot(models.Model):
    event_name = models.CharField(max_length=100, default='Event')
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
    volunteer = models.ManyToManyField(CustomUser)
    user = models.ManyToManyField(User)
    corporate_registered_users = models.ManyToManyField(CustomUser, related_name='corporate_registered_users')
    business_name = models.ForeignKey(Business, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.event_name

class CurrentTimeSlots(models.Model):
    current_id = models.IntegerField(default=0)
    current_date = models.DateField(auto_now=True)
    last_update = models.DateField(default='1900-01-02')
    current_timeslots = models.ManyToManyField(TimeSlot)

    def current_all(self):
        timeslots = TimeSlot.objects.all()
        today = datetime.now().date()
        for i in timeslots:
            if i.date >= today:
                self.current_timeslots.add(i)
            else:
                self.current_timeslots.remove(i)

    def current(self):
        all_current = self.current_timeslots.all()
        today = datetime.now().date()
        for i in all_current:
            if i.date >= today:
                self.current_timeslots.add(i)
            else:
                self.current_timeslots.remove(i)


