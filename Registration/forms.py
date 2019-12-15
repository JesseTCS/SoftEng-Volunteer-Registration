from django import forms
from django.contrib.auth.forms import AuthenticationForm

class EmailForm(forms.Form):
    """
    Form for collecting unregistered user data.
    """
    email = forms.EmailField()
    birthday = forms.DateField(input_formats=['%b-%d-%y'])
    area_code = forms.CharField(max_length=3, min_length=3)
    numbers1 = forms.CharField(max_length=3, min_length=3)
    numbers2 = forms.CharField(max_length=4, min_length=4)

class UserForm(forms.Form):
    Username = forms.CharField()

class TimeForm(forms.Form):
    TimeSlot = forms.IntegerField()

class csvForm(forms.Form):
    csv = forms.FileField()

class Message_Form(forms.Form):
    message_form = forms.TimeField(widget=forms.Textarea)

class timeslotForm(forms.Form):
    ACTIVITY_CHOICES = (
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
        )
    event_name = forms.CharField()
    date = forms.DateField(widget=forms.SelectDateWidget())
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
    business_name = forms.CharField(max_length=100)
    barea_code = forms.CharField(max_length=3,help_text='test')
    bnumbers1 = forms.CharField(max_length=3)
    bnumbers2 = forms.CharField(max_length=4)
    baddress1 = forms.CharField()
    baddress2 = forms.CharField()
    bcity = forms.CharField()
    bstate = forms.CharField()
    bzip_code = forms.CharField()
    bcountry = forms.CharField()

class createUserForm(forms.Form):
    username = forms.CharField(min_length=3)
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)
    email = forms.EmailField()
    birthday = forms.DateField()
    birthday = forms.DateField(input_formats=['%b-%d-%y'])
    area_code = forms.CharField(max_length=3, min_length=3)
    numbers1 = forms.CharField(max_length=3, min_length=3)
    numbers2 = forms.CharField(max_length=4, min_length=4)

class AuthenticationFormWithInactiveUsersOkay(AuthenticationForm):
    def confirm_login_allowed(self, user):
        pass