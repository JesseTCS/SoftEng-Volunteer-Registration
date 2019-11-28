from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import TimeSlot
from .forms import EmailForm
import random
import string

# Create your views here.
def home(request):
    TimeSlots = TimeSlot.objects
    return render(request, 'Registration/home.html', {'TimeSlots': TimeSlots})

def details(request, id):
    # add send email and increment Timeslot item
    form = EmailForm()
    TimeSlot_detail = get_object_or_404(TimeSlot, pk=id)
    return render(request, 'Registration/detail.html', {'TimeSlot': TimeSlot_detail, 'form':form})

def thanks(request):
    sendemail(request)
    return render(request, 'Registration/thanks.html')


def sendemail(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            sendto = form.cleaned_data['their_email']
            if User.objects.get(username=sendto[:sendto.index('@')]):
                send_mail('Registration',
                f'Thank you for registering.',
                'jessethomascs@gmail.com',
                [sendto],)
            else:
                tempPassword = createTempPassword()
                createUser(sendto, tempPassword)
                send_mail('Registration',
                f'Thank you for registering. This is your temporary password: {tempPassword}',
                'jessethomascs@gmail.com',
                [sendto],)
    else:
        form = EmailForm()

def createTempPassword(stringLength=10):
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(password_characters) for i in range(stringLength))

def createUser(email, tempPassword):
    username = email[:email.index('@')]
    user = User.objects.create_user(username, sendto, tempPassword)
    user.save()

def nothing(request):
    return render(request, 'Registration/profile.html')

