from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from .models import TimeSlot, Address
from .forms import EmailForm, UserForm, TimeForm, csvForm, timeslotForm
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
    return render(request, 'Registration/thanks.html')


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
        email = form.cleaned_data['Enter_your_email_to_register']
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
        email = form.cleaned_data['Enter_your_email_to_register']
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
        email = form.cleaned_data['Enter_your_email_to_register']
        userAndPass = createUser(email)
        userAccount = userAndPass[0]
        tempPassword = userAndPass[1]
        if verifyTimeSlotAvailability(userAccount, timeslot):
            timeslot.volunteer.add(userAccount)
            sendemail(userAccount, timeslot, tempPassword, newUser=True)
            return True
        else:
            return False

def profile(request):
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
    form_web = timeslotForm()
    success = 'Submission Successful'
    prompt = {
        'order': 'Order of csv should be event name, date (eg. Jan 01, 1960), start time (eg. 6:54 pm), end time, activity level (L,M,H), description, number of needed, v',
        'form':form,
        'form_web':form_web,
        'success':success
    }
    if request.method == 'GET':
        return render(request, template, prompt)
    context={}
    if not request.FILES:
        create_time_slot(request)
        return render(request, template, context)
    csv_file = request.FILES['csv']
    if not csv_file.name.endswith('.csv'):
        messages.error(request, 'This is not a csv file')
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        create_time_slot(column=True, column_data=column)
    return render(request, template, context)

def create_time_slot(request = False, column = False, column_data = False):
        if column:
            create_time_slot_csv(column_data)
        else:
            create_time_slot_web(request)

def create_time_slot_csv(column_data):
    date_format = '%b-%d-%y'
    time_format = '%I:%M %p'
    Event_Name=column_data[0]
    date=datetime.strptime(column_data[1], date_format)
    start_time=datetime.strptime(column_data[2], time_format)
    end_time=datetime.strptime(column_data[3], time_format)
    description=column_data[4]
    num_needed=int(column_data[5])
    activity_level=column_data[6]
    address1 = column_data[7]
    address2 = column_data[8]
    city = column_data[9]
    state = column_data[10]
    zip_code = column_data[11]
    country = column_data[12]
    address = create_address(address1, address2, city, state, zip_code, country)
    if start_time<end_time:
        if TimeSlot.objects.filter(Event_Name=Event_Name, date=date, start_time=start_time, address=address):
            timeslot = TimeSlot.objects.filter(Event_Name=Event_Name, date=date, start_time=start_time, address=address)[0]
            update_existing_time_slot(timeslot, Event_Name, date, start_time, end_time, description, num_needed, activity_level, address)
        if check_time_slot_availablity(date,start_time,end_time,address):
            create = TimeSlot.objects.update_or_create(
                Event_Name=Event_Name,
                date=date,
                start_time=start_time,
                end_time=end_time,
                description=description,
                num_needed=num_needed,
                activity_level=activity_level,
                address = address
            )


def create_time_slot_web(request):
    form = timeslotForm(request.POST)
    if form.is_valid():
        Event_Name = form.cleaned_data['Event_Name']
        date = form.cleaned_data['date']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        activity_level = form.cleaned_data['activity_level']
        description = form.cleaned_data['description']
        num_needed = form.cleaned_data['num_needed']
        address1 = form.cleaned_data['address1']
        address2 = form.cleaned_data['address2']
        city = form.cleaned_data['city']
        state = form.cleaned_data['state']
        zip_code = form.cleaned_data['zip_code']
        country = form.cleaned_data['country']
        address = create_address(address1, address2, city, state, zip_code, country)
        if start_time<end_time:
            if TimeSlot.objects.filter(Event_Name=Event_Name, date=date, start_time=start_time, address=address):
                timeslot = TimeSlot.objects.filter(Event_Name=Event_Name, date=date, start_time=start_time, address=address)[0]
                update_existing_time_slot(timeslot, Event_Name, date, start_time, end_time, description, num_needed, activity_level, address)
            if check_time_slot_availablity(date,start_time,end_time,address):
                create = TimeSlot.objects.update_or_create(
                    Event_Name=Event_Name,
                    date=date,
                    start_time=start_time,
                    end_time=end_time,
                    description=description,
                    num_needed=num_needed,
                    activity_level=activity_level,
                    address = address
                )


def create_address(address1=None,address2=None,city=None,state=None,zip_code=None,country=None):
    create = Address.objects.update_or_create(
        address1 = address1,
        address2 = address2,
        city = city,
        state = state,
        zip_code = zip_code,
        country = country
    )
    return create[0]

def update_existing_time_slot(timeslot, Event_Name, date, start_time, end_time, description, num_needed, activity_level, address):
    timeslot.Event_Name=Event_Name,
    timeslot.date=date,
    timeslot.start_time=start_time,
    timeslot.end_time=end_time,
    timeslot.description=description,
    timeslot.num_needed=num_needed,
    timeslot.activity_level=activity_level,
    timeslot.address = address

def check_time_slot_availablity(date,start_time,end_time,address):
    same_date_and_address_time_slot = TimeSlot.objects.filter(date=date, address=address)
    for timeslot in same_date_and_address_time_slot:
        if timeslot.start_time > start_time.time() and timeslot.start_time > end_time.time():
            return True
        elif timeslot.end_time < start_time.time() and timeslot.end_time < end_time.time():
            return True
        return False
    return True