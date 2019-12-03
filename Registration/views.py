from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from .models import TimeSlot
from .forms import EmailForm, UserForm, TimeForm, csvForm, addressForm
from datetime import datetime
import random, string, csv, io

# Create your views here.
def home(request):
    TimeSlots = TimeSlot.objects
    for timeslot in TimeSlots.all():
        modifyCount(timeslot)
    return render(request, 'Registration/home.html', {'TimeSlots': TimeSlots})

def details(request, id):
    # add send email and increment Timeslot item
    TimeSlot_detail = get_object_or_404(TimeSlot, pk=id)
    invalid = False
    form = EmailForm()
    if request.method == 'POST':
        if loggedIn(request):
            if registerLoggedInUser(request, TimeSlot_detail):
                return redirect('thanks')
            else:
                invalid = True
                return render(request, 'Registration/detail.html', {'TimeSlot': TimeSlot_detail, 'form':form, 'invalid':invalid})
        elif userExists(request):
            if registerExistingUser(request, TimeSlot_detail):
                return redirect('thanks')
            else:
                invalid = True
                return render(request, 'Registration/detail.html', {'TimeSlot': TimeSlot_detail, 'form':form, 'invalid':invalid})
        else:
            if registerNewUser(request, TimeSlot_detail):
                return redirect('thanks')
            else:
                invalid = True
                return render(request, 'Registration/detail.html', {'TimeSlot': TimeSlot_detail, 'form':form, 'invalid':invalid})
    modifyCount(TimeSlot_detail)
    return render(request, 'Registration/detail.html', {'TimeSlot': TimeSlot_detail, 'form':form, 'invalid':invalid})

def thanks(request):
    return render(request, 'Registration/thanks.html', {'form':form})


def sendemail(userAccount,timeslot,tempPassword=0,newUser=False):
    if newUser:
        send_mail('Volunteer Registration',
            f'Thank you for registering. This is your temporary password: {tempPassword}. Follow this link',
            'jessethomascs@gmail.com',
            [userAccount.email],)
    else:
        send_mail('Registration',
            f'Thank you for registering.',
            'jessethomascs@gmail.com',
            [userAccount.email],)

def createTempPassword(stringLength=10):
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(password_characters) for i in range(stringLength))

def createUser(email):
    username = email[:email.index('@')]
    tempPassword = createTempPassword()
    userAccount = User.objects.create_user(username, email, tempPassword)
    userAccount.save()
    return (userAccount, tempPassword)

def verifyTimeSlotAvailability(userAccount, timeslot, batch_number = 0):
    if timeslot.volunteer.filter(username=userAccount.username):
        return False
    elif (timeslot.num_signed_up+batch_number) > timeslot.num_needed:
        return False
    elif timeslot.num_signed_up+1 > timeslot.num_needed:
        return False
    return True

def verifyUserAvailabilityForTimeSlot(TimeSlot_detail):
    pass

def modifyCount(timeslot):
    timeslot.num_signed_up = timeslot.volunteer.all().count()
    timeslot.save()

def loggedIn(request):
    form = EmailForm(request.POST)
    if form.is_valid():
        return False
    return True

def userExists(request):
    form = EmailForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['Enter your email to register']
        try:
            userAccount = User.objects.get(email=email)
            return True
        except:
            return False

def registerLoggedInUser(request, timeslot):
    form = UserForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['Username'][:-1]
        userAccount = User.objects.get(username=username)
        if verifyTimeSlotAvailability(userAccount, timeslot):
            timeslot.volunteer.add(userAccount)
            sendemail(userAccount, timeslot)
            return True
        else:
            return False

def registerExistingUser(request, timeslot):
    form = EmailForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['Enter your email to register']
        userAccount = User.objects.get(email=email)
        if verifyTimeSlotAvailability(userAccount, timeslot):
            timeslot.volunteer.add(userAccount)
            sendemail(userAccount, timeslot)
            return True
        else:
            return False

def registerNewUser(request, timeslot):
    form = EmailForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['Enter your email to register']
        userAndPass = createUser(email)
        userAccount = userAndPass[0]
        tempPassword = userAndPass[1]
        if verifyTimeSlotAvailability(userAccount, timeslot):
            timeslot.volunteer.add(userAccount)
            sendemail(userAccount, timeslot, tempPassword, newUser=True)
            return True
        else:
            return False

def nothing(request):
    return render(request, 'Registration/profile.html')

@login_required
def dashboard(request):
    if request.method == 'POST':
        unregisterUser(request)
    return render(request, 'Registration/dashboard.html')

def unregisterUser(request):
    form = UserForm(request.POST)
    if form.is_valid():
        userAccount = form.cleaned_data['Username']
        userAccount = User.objects.get(username=userAccount)
        form = TimeForm(request.POST)
        if form.is_valid():
            id = form.cleaned_data['TimeSlot']
            timeslot = TimeSlot.objects.get(id=id)
            timeslot.volunteer.remove(userAccount)
            modifyCount(timeslot)

def logout(request):
    return render(request, 'Registration/logout.html')

@permission_required('admin.can_add_log_entry')
def timelot_upload(request):
    template = 'Registration/upload.html'
    form = csvForm()
    prompt = {
        'order': 'Order of csv should be event name, date (eg. Jan 01, 1960), start time (eg. 6:54 pm), end time, activity level (L,M,H), description, number of needed, v',
        'form':form
    }
    date_format = '%b-%d-%y'
    time_format = '%I:%M %p'
    if request.method == 'GET':
        return render(request, template, prompt)
    csv_file = request.FILES['csv']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file')
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        create = TimeSlot.objects.update_or_create(
            Event_Name=column[0],
            date=datetime.strptime(column[1], date_format),
            start_time=datetime.strptime(column[2], time_format),
            end_time=datetime.strptime(column[3], time_format),
            description=column[4],
            num_needed=int(column[5]),
            activity_level=column[6],
        )
    context={}
    return render(request, template, context)