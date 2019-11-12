from django.db import models

# Create your models here.
class TimeSlot(models.Model):
    ACTIVITY_CHOICES = (
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
        )
    date_time = models.DateTimeField()
    activity_level = models.CharField(max_length=1, choices=ACTIVITY_CHOICES)
    number_available = models.Model
    description = models.TextField()