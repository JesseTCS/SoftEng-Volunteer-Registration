from django import forms
from django.contrib.auth.forms import AuthenticationForm

class EmailForm(forms.Form):
    their_email = forms.EmailField()

class AuthenticationFormWithInactiveUsersOkay(AuthenticationForm):
    def confirm_login_allowed(self, user):
        pass