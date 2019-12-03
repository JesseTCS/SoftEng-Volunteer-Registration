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

class addressForm(forms.Form):
  street_number = forms.CharField()
  route = forms.CharField()
  locality = forms.CharField()
  administrative_area_level_1 = forms.CharField()
  country = forms.CharField()
  postal_code = forms.CharField()

class AuthenticationFormWithInactiveUsersOkay(AuthenticationForm):
    def confirm_login_allowed(self, user):
        pass