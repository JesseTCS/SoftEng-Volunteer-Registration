from django import forms
from django.contrib.auth.forms import AuthenticationForm

class EmailForm(forms.Form):
    Enter_your_email_to_register = forms.EmailField()

class UserForm(forms.Form):
    Username = forms.CharField()

class TimeForm(forms.Form):
    TimeSlot = forms.IntegerField()

class csvForm(forms.Form):
    csv = forms.FileField()

class timeslotForm(forms.Form):
    ACTIVITY_CHOICES = (
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
        )
    Event_Name = forms.CharField()
    date = forms.DateField(input_formats=['%b-%d-%y'],help_text='Ex: Jan-01-2019')
    start_time = forms.TimeField(input_formats=['%I:%M %p'], help_text='Ex: 07:00 PM')
    end_time = forms.TimeField(input_formats=['%I:%M %p'], help_text='Ex: 08:00 PM')
    activity_level = forms.CharField(widget=forms.Select(choices=ACTIVITY_CHOICES))
    description = forms.CharField()
    num_needed = forms.IntegerField()
    address1 = forms.CharField()
    address2 = forms.CharField()
    city = forms.CharField()
    state = forms.CharField()
    zip_code = forms.CharField()
    country = forms.CharField()

class AuthenticationFormWithInactiveUsersOkay(AuthenticationForm):
    def confirm_login_allowed(self, user):
        pass