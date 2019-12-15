from django.contrib import admin
from .models import TimeSlot, Address, Business, PhoneNumber, CustomUser

# Register your models here.
admin.site.register(TimeSlot)
admin.site.register(Address)
admin.site.register(Business)
admin.site.register(PhoneNumber)
admin.site.register(CustomUser)