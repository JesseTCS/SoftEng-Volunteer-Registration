from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
from .models import TimeSlot, Address, CustomUser, PhoneNumber, Business
from .forms import EmailForm, UserForm, TimeForm, csvForm, timeslotForm, Message_Form, createUserForm
from datetime import datetime
import random, string, csv, io

# Create your views here.
def home(request):
    """
    Used to display the homepage
    """
    timeslots = all_time_slots=TimeSlot.objects.all()
    mass_update_count(timeslots)
    return render(request, 'Registration/home.html', {'timeslots': timeslots})

def details(request, id):
    """
    Shows the details of a specific timeslot.
    """
    timeslot = timeslot=get_object_or_404(TimeSlot, pk=id)
    email_form = EmailForm()
    unregister_flag = 0
    register_flag = 0
    error_0 = 'Age Restriction'
    error_1 = 'Email Taken'
    error_2 = 'Timeslot Conlicts with Registered Timeslots'
    error_3 = 'Timeslot unavailable'
    error_message = 'Sorry, we could not perform this action due to: '
    if request.method == 'GET':
        if request.user.is_authenticated:
            if timeslot.user.filter(username=request.user.username):
                unregister_flag = 1
            else: 
                register_flag = 1
        update_count(timeslot)
        return render(request, 'Registration/detail.html', {'timeslot': timeslot, 'email_form': email_form, 'unregister_flag':unregister_flag, 'register_flag': register_flag})
    else:
        invalid = False
        if 'unregister' in request.POST:
            unregister(request, timeslot)
            update_count(timeslot)
            register_flag = 1
            return render(
            request,
            'Registration/detail.html', 
            {'timeslot': timeslot,
            'email_form': email_form,
            'invalid': invalid,
            'unregister_flag':unregister_flag,
            'register_flag': register_flag
            })
        if 'register' in request.POST:
            register_flag = 1
            if timeslot_count_check(timeslot=timeslot):
                register = registerfunc(request, timeslot)
                if register == error_2:
                    invalid = True
                    return render(
                    request,
                    'Registration/detail.html', 
                    {'timeslot': timeslot,
                    'email_form': email_form,
                    'invalid': invalid,
                    'unregister_flag':unregister_flag,
                    'register_flag': register_flag,
                    'error_code': error_2
                    })
                update_count(timeslot)
                register_flag = 0
                unregister_flag = 1
                return redirect('thanks')
            invalid = True
            return render(
                request,
                'Registration/detail.html', 
                {'timeslot': timeslot,
                'email_form': email_form,
                'invalid': invalid,
                'unregister_flag':unregister_flag,
                'register_flag': register_flag,
                'error_code': error_3
            })
        if 'new_user' in request.POST:
            if timeslot_count_check(timeslot=timeslot):
                register = register_new_user(request, timeslot)
                if register == error_0:
                    invalid = True
                    return render(
                    request,
                    'Registration/detail.html', 
                    {'timeslot': timeslot,
                    'email_form': email_form,
                    'invalid': invalid,
                    'unregister_flag':unregister_flag,
                    'register_flag': register_flag,
                    'error_message': error_message,
                    'error_code': error_0
                    })
                if register == error_1:
                    invalid = True
                    return render(
                    request,
                    'Registration/detail.html', 
                    {'timeslot': timeslot,
                    'email_form': email_form,
                    'invalid': invalid,
                    'unregister_flag':unregister_flag,
                    'register_flag': register_flag,
                    'error_message': error_message,
                    'error_code': error_1
                    })
                return redirect('thanks')
                raise Exception('details')
            invalid = True
            return render(
                request,
                'Registration/detail.html', 
                {'timeslot': timeslot,
                'email_form': email_form,
                'invalid': invalid,
                'unregister_flag':unregister_flag,
                'register_flag': register_flag,
                'error_code': error_3
            })
        if 'register_group' in request.POST:
            return redirect('group_register', id)

def group_register(request, id):
    timeslot = get_object_or_404(TimeSlot, pk=id)
    error = None
    error_0 = 'File not a CSV'
    error_1 = 'New timeslot conflicts with existing'
    template = 'Registration/group_register.html'
    form = csvForm()
    form_web = timeslotForm()
    success = False
    success_message = 'Submission Successful'
    invalid = False
    order = [
        "Upload a list of emails with 'email' as comlumn header",
    ]
    prompt = {
        'order': order[0],
        'form':form,
        'invalid': invalid,
        'error_code': error,
        'success': success,
        'success_message': success_message,
    }
    if request.method == 'GET':
        return render(request, template, prompt)
    csv_file = request.FILES['csv']
    last4 = csv_file.name[-4:]
    if last4 != '.csv':
        invalid = True
        error = error_0
        prompt['invalid'] = invalid
        prompt['error_code'] = error
        return render(request, template, prompt)
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    array = []
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        array.append([column[0],column[1],column[2]])
    number_of_elements = len(array)
    # if timeslot.num_signed_up + number_of_elements > timeslot.num_needed:
        # messages.error(request, 'Group to large for timeslot')
        # raise Exception("group_register_0")
    for i in array:
        exists = user_exists(email=i[0])
        if exists[0]:
            user_account = exists[1]
            custom_account = CustomUser.objects.get(user_account=user_account)
            if timeslot_available_to_user(request=None, custom_account=custom_account, timeslot=timeslot):
                continue
                register_group(user_account=user_account, timeslot=timeslot)
            else:
                continue
                raise Exception('group_register_1')
        else:
            phone_number = create_phone_number(phone_number=i[2])
            birthday = create_birthday(i[1])
            temp_password = create_temp_password(stringLength=10)
            username = i[0][:i[0].index('@')]
            email = i[0]
            custom_user = create_user_from_group_upload(username=username,temp_password=temp_password,email=email,birthday=birthday,phone_number=phone_number)
            register_group(request=request, custom_user=custom_user, timeslot=timeslot, temp_password=temp_password)
    return render(request, template, prompt)

@login_required
def dashboard(request):
    if request.method == 'POST':
        timeslot_id = request.POST['timeslot']
        timeslot = TimeSlot.objects.get(id=timeslot_id)
        unregister(request, timeslot)
    return render(request, 'Registration/dashboard.html')

def thanks(request):
    return render(request, 'Registration/thanks.html')

def create_user(request):
    template = 'Registration/create_user.html'
    invalid = False
    error = None
    error_0 = 'Age Restriction'
    error_1 = 'Email Taken'
    error_2 = 'Username Taken'
    create_user_form = createUserForm()
    context = {
        'invalid': invalid,
        'error_code': error,
        'create_user_form': create_user_form
    }
    if request.method == 'POST':
        cleaned_form = clean_create_user_form(request)
        if cleaned_form:
            username = cleaned_form[0]
            password = cleaned_form[1]
            email = cleaned_form[2]
            birthday = cleaned_form[3]
            area_code = cleaned_form[4]
            numbers1 = cleaned_form[5]
            numbers2 = cleaned_form[6]
            valid_age = age_check(birthday)
            if valid_age:
                result = user_exists(username=username,email=email)
                exists = result[0]
                if exists:
                    if result[2] == 'email':
                        error = error_1
                    elif result[2] == 'username':
                        error = error_2
                else:
                    phone_number = create_phone_number(area_code, numbers1, numbers2)
                    create_user_from_create_user(username, password, email, birthday, phone_number)
                    return redirect('login')
            else:
                error = error_0
            
            invalid = True
            context['invalid'] = invalid
            context['error_code'] = error
            return render(request, template, context)
    return render(request, template, context)

@permission_required('admin.can_add_log_entry')
def timelot_upload(request):
    #21 spots 
    error = None
    error_0 = 'File not a CSV'
    error_1 = 'New timeslot conflicts with existing'
    template = 'Registration/upload.html'
    form = csvForm()
    form_web = timeslotForm()
    success = False
    success_message = 'Submission Successful'
    invalid = False
    timeslot = ''
    order = [
        'In order to upload csv files the order of the csv header should be as follows:',
        'Event Name, Date(Jan-01-20), Start Time(11:59 PM), End Time(6:00 AM), Description, Number of Volunteers needed, "Activity Level(L.M.H)", Address 1, Address 2, City, State, Zip Code, Country, Business Name, Business Address 1, Business Address 2, Business City, Business State, Business Zip Code, Business Country, Business Phone Number'
    ]
    prompt = {
        'order_message_0': order[0],
        'order': order[1],
        'form':form,
        'form_web':form_web,
        'invalid': invalid,
        'error_code': error,
        'success': success,
        'success_message': success_message,
        'timeslot':timeslot
    }
    if request.method == 'GET':
        return render(request, template, prompt)
    context={}
    if request.FILES:
        test = False
        csv_file = request.FILES['csv']
        last4 = csv_file.name[-4:]
        if last4 != '.csv':
            invalid = True
            error = error_0
            prompt['invalid'] = invalid
            prompt['error_code'] = error
            return render(request, template, prompt)
        data_set = csv_file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=','):
            timeslot_dict = sort_csv_data(column)
            address = create_address(
                address1 = timeslot_dict['address1'], 
                address2 = timeslot_dict['address2'], 
                city = timeslot_dict['city'], 
                state = timeslot_dict['state'], 
                zip_code = timeslot_dict['zip_code'], 
                country = timeslot_dict['country']
            )
            if timeslot_dict['baddress1'] is not None:
                baddress = create_address(
                    address1 = timeslot_dict['baddress1'], 
                    address2 = timeslot_dict['baddress2'], 
                    city = timeslot_dict['bcity'], 
                    state = timeslot_dict['bstate'], 
                    zip_code = timeslot_dict['bzip_code'], 
                    country = timeslot_dict['bcountry']
                )
            if timeslot_dict['baddress1'] is not None:
                bphone_number = create_phone_number(phone_number = timeslot_dict['bphone_number'])
                # bphone_number = create_phone_number(area_code=timeslot_dict['barea_code'], numbers1=timeslot_dict['bnumbers1'], numbers2=timeslot_dict['bnumbers2'])
            if timeslot_dict['business_name'] is not None:
                business = create_business(timeslot_dict['business_name'],baddress,bphone_number)
            timeslot = create_timeslot(
                event_name = timeslot_dict['event_name'], 
                date = timeslot_dict['date'], 
                start_time = timeslot_dict['start_time'], 
                end_time = timeslot_dict['end_time'], 
                address = address, 
                activity_level = timeslot_dict['activity_level'], 
                description = timeslot_dict['description'], 
                num_needed = timeslot_dict['num_needed'], 
                business_name = business
            )
            if timeslot[0] == error_1:
                invalid = True
                error = error_1
                prompt['invalid'] = invalid
                prompt['error_code'] = error
                prompt['timeslot'] = str(timeslot[1])
                return render(request, template, prompt)
        success = True
        prompt['success'] = success
        return render(request, template, prompt)
    if not request.FILES:
        timeslot_dict = sort_request_data(request)
        address = create_address(
            address1 = timeslot_dict['address1'], 
            address2 = timeslot_dict['address2'], 
            city = timeslot_dict['city'], 
            state = timeslot_dict['state'], 
            zip_code = timeslot_dict['zip_code'], 
            country = timeslot_dict['country']
        )
        if timeslot_dict['baddress1'] is not None:
            baddress = create_address(
                address1 = timeslot_dict['baddress1'], 
                address2 = timeslot_dict['baddress2'], 
                city = timeslot_dict['bcity'], 
                state = timeslot_dict['bstate'], 
                zip_code = timeslot_dict['bzip_code'], 
                country = timeslot_dict['bcountry']
            )
        if timeslot_dict['baddress1'] is not None:
            bphone_number = create_phone_number(area_code=timeslot_dict['barea_code'], numbers1=timeslot_dict['bnumbers1'], numbers2=timeslot_dict['bnumbers2'])
        if timeslot_dict['business_name'] is not None:
            business = create_business(timeslot_dict['business_name'],baddress,bphone_number)
        timeslot = create_timeslot(
            event_name = timeslot_dict['event_name'], 
            date = timeslot_dict['date'], 
            start_time = timeslot_dict['start_time'], 
            end_time = timeslot_dict['end_time'], 
            address = address, 
            activity_level = timeslot_dict['activity_level'], 
            description = timeslot_dict['description'], 
            num_needed = timeslot_dict['num_needed'], 
            business_name = business
        )
        if timeslot[0] == error_1:
            invalid = True
            error = error_1
            prompt['invalid'] = invalid
            prompt['error_code'] = error
            prompt['timeslot'] = str(timeslot[1])
            return render(request, template, prompt)
    success = True
    prompt['success'] = success
    return render(request, template, prompt)

def mass_update_count(timeslots):
    """
    Updates volunteer count over many timeslots
    """
    for i in timeslots:
        update_count(i)

def update_count(timeslot):
    """
    Updates volunteer count on one timeslot
    """
    timeslot.num_signed_up = timeslot.volunteer.all().count()
    timeslot.save()

def registerfunc(request, timeslot):
    error_2 = 'Timeslot Conlicts with Registered Timeslots'
    user_account = request.user
    custom_account = CustomUser.objects.get(user_account=user_account)
    if timeslot_available_to_user(request=request, custom_account=custom_account, timeslot=timeslot):
        timeslot.volunteer.add(custom_account)
        timeslot.user.add(user_account)
        sendmail(user_account, timeslot)
        return
    return error_2

def unregister(request, timeslot):
    username = request.POST['unregister']
    user_account = User.objects.get(username=username)
    custom_account = CustomUser.objects.get(user_account=user_account)
    timeslot.volunteer.remove(custom_account)
    timeslot.corporate_registered_users.remove(custom_account)
    timeslot.user.remove(user_account)
    timeslot.save()

def register_new_user(request, timeslot):
    option_1 = 'create_from_email'
    error_0 = 'Age Restriction'
    error_1 = 'Email Taken'
    if request.POST['new_user'] == option_1:
        if user_exists(request)[0]:
            return  error_1
            raise Exception('register_new_user_0')
        new_user = create_user_from_email(request)
        if new_user == error_0:
            return error_0
        timeslot.volunteer.add(new_user[0])
        sendmail(new_user[1], timeslot, new_user[2], True)
        return
    raise Exception('register_new_user1')

def register_group(request=None, custom_user=None, timeslot=None, temp_password =None):
    timeslot.volunteer.add(custom_user)
    timeslot.corporate_registered_users.add(custom_user)
    timeslot.save()
    sendmail(user_account=custom_user.user_account,timeslot=timeslot,temp_password=temp_password,new_user=True)
    return
    raise Exception('register_group')


def create_user_from_email(request):
    cleaned_email_form_data = clean_email_form(request)
    error_0 = 'Age Restriction'
    if cleaned_email_form_data == error_0:
        return error_0
    email = cleaned_email_form_data[0]
    birthday = cleaned_email_form_data[1]
    area_code = cleaned_email_form_data[2]
    numbers1 = cleaned_email_form_data[3]
    numbers2 = cleaned_email_form_data[4]
    phone_number = create_phone_number(area_code, numbers1, numbers2)
    username = email[:email.index('@')]
    temp_password = create_temp_password()
    user_account = User.objects.create_user(username, email, temp_password)
    user_account.save()
    custom_user = CustomUser.objects.update_or_create(user_account = user_account, birthday = birthday)[0]
    custom_user.phone_number.add(phone_number)
    custom_user.save()
    return (custom_user, user_account, temp_password)
    raise Exception('create_user_from_email_0')
    raise Exception('create_user_from_email_1')

def create_user_from_create_user(username,password,email,birthday,phone_number):
    user_account = User.objects.create_user(username,email,password)
    user_account.save()
    custom_user = CustomUser.objects.update_or_create(user_account = user_account, birthday = birthday)[0]
    custom_user.phone_number.add(phone_number)
    custom_user.save()

def create_user_from_group_upload(username=None,temp_password=None,email=None,birthday=None,phone_number=None):
    suffic = 1
    username_temp = username
    while(1):
        try:
            user_account = User.objects.create_user(username,email,temp_password)
            break
        except:
            suffic += 1
            username = username_temp + str(suffic)
        
    user_account.save()
    custom_user = CustomUser.objects.update_or_create(user_account = user_account, birthday = birthday)[0]
    custom_user.phone_number.add(phone_number)
    custom_user.save()
    return custom_user
    raise Exception('create_user_from_group_upload_0')

def create_temp_password(stringLength=10):
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(password_characters) for i in range(stringLength))

def create_birthday(birthday=None):
    date_format = '%b-%d-%y'
    date = datetime.strptime(birthday, date_format)
    return date

def create_phone_number(area_code=None, numbers1=None, numbers2=None, phone_number=None):
    if phone_number:
        phone_number = phone_number.split('-')
        area_code = phone_number[0]
        numbers1 = phone_number[1]
        numbers2 = phone_number[2]
    phone_number = PhoneNumber.objects.update_or_create(
            area_code = area_code,
            numbers1 = numbers1,
            numbers2 = numbers2
        )[0]
    phone_number.save()
    return phone_number

def create_address(address1, address2, city, state, zip_code, country):
    address = Address.objects.update_or_create(
        address1 = address1, 
        address2 = address2, 
        city = city, 
        state = state, 
        zip_code = zip_code, 
        country = country)[0]
    address.save()
    return address

def create_business(business_name, address, phone_number):
    business = Business.objects.update_or_create(
        business_name = business_name,
        address = address,
    )[0]
    business.phone_number.add(phone_number)
    business.save()
    return business

def create_timeslot(event_name, date, start_time, end_time, address, activity_level, description, num_needed, business_name):
    error = None
    error_0 = 'New timeslot conflicts with existing'
    date_format = '%b-%d-%y'
    time_format = '%I:%M %p'
    form = True
    if type(date) is str:
        date = datetime.strptime(date, date_format)
        form=False
    if type(start_time) is str:
        start_time = datetime.strptime(start_time, time_format)
        form = False
    if type(end_time) is str:
        form = False
        end_time = datetime.strptime(end_time, time_format)
    conflict = timeslot_creation_conflict(date, start_time, end_time, address, form)
    if conflict[0]:
        timeslot = TimeSlot.objects.update_or_create(
            event_name = event_name, 
            date = date, 
            start_time = start_time, 
            end_time = end_time, 
            address = address, 
            activity_level= activity_level, 
            description = description, 
            num_needed = num_needed, 
            business_name = business_name
        )[0]
        timeslot.save()
        return (None, timeslot)
    else:
        error = error_0
        return (error, conflict[1], date, start_time, end_time, address)

def timeslot_creation_conflict(date, start_time, end_time, address, form=None):
    if form:
        timeslots = TimeSlot.objects.filter(date=date,address=address)
        for timeslot in timeslots:
            if start_time < timeslot.start_time and end_time > timeslot.start_time and start_time < timeslot.end_time and end_time <= timeslot.end_time:
                return (False, timeslot, 0)
            elif start_time <= timeslot.start_time and end_time > timeslot.start_time and start_time < timeslot.end_time and end_time >= timeslot.end_time:
                return (False, timeslot, 1)
            elif start_time >= timeslot.start_time and end_time > timeslot.start_time and start_time < timeslot.end_time and end_time > timeslot.end_time:
                return (False, timeslot, 2)
        return (True, None)
    else:
        timeslots = TimeSlot.objects.filter(date=date.date(),address=address)
        for timeslot in timeslots:
            if start_time.time() < timeslot.start_time and end_time.time() > timeslot.start_time and start_time.time() < timeslot.end_time and end_time.time() <= timeslot.end_time:
                return (False, timeslot, 0)
            elif start_time.time() <= timeslot.start_time and end_time.time() > timeslot.start_time and start_time.time() < timeslot.end_time and end_time.time() >= timeslot.end_time:
                return (False, timeslot, 1)
            elif start_time.time() >= timeslot.start_time and end_time.time() > timeslot.start_time and start_time.time() < timeslot.end_time and end_time.time() > timeslot.end_time:
                return (False, timeslot, 2)
        return (True, None)

def age_check(birthday):
    today = datetime.today()
    years = today.year - birthday.year
    if today.month < birthday.month or (today.month == birthday.month and today.day < birthday.day):
        years -= 1
    age = years
    if age < 18:
        return False
    return True
    raise Exception('create_user_from_email_1')

def user_exists(request=None,username=None,email=None):
    if request:
        email = request.POST['email']
        if User.objects.filter(email=email):
            user_account = User.objects.get(email=email)
            return (True, user_account)
        return (False, None)
    elif User.objects.filter(email=email):
        user_account = User.objects.get(email=email)
        return (True, user_account, 'email')
    elif User.objects.filter(username=username):
        user_account = User.objects.get(username=username)
        return (True, user_account, 'username')
    else:
        return (False, None, None)
    

def unique_email(request):
    pass

def timeslot_available_to_user(request=None, custom_account=None, timeslot=None):
    if request and request.method == 'POST':
        user_account = request.user
    else:
        user_account = custom_account.user_account
    if timeslot.volunteer.filter(user_account=user_account):
        return False
    else:
        timeslots = TimeSlot.objects.filter(volunteer=custom_account, date = timeslot.date)
        for i in timeslots:
            if i.start_time < timeslot.start_time and i.end_time > timeslot.start_time and i.start_time < timeslot.end_time and i.end_time <= timeslot.end_time:
                return False
            elif i.start_time <= timeslot.start_time and i.end_time > timeslot.start_time and i.start_time < timeslot.end_time and i.end_time >= timeslot.end_time:
                return False
            elif i.start_time >= timeslot.start_time and i.end_time > timeslot.start_time and i.start_time < timeslot.end_time and i.end_time > timeslot.end_time:
                return False
        return True

def timeslot_count_check(timeslot=None, count=1):
    if timeslot.num_signed_up + count > timeslot.num_needed:
        return False
    return True

def clean_email_form(request):
    error = None
    email_form = EmailForm(request.POST)
    if email_form.is_valid():
        email = email_form.cleaned_data['email']
        birthday = email_form.cleaned_data['birthday']
        valid_age = age_check(birthday)
        if valid_age:
            area_code = str(email_form.cleaned_data['area_code'])
            numbers1 = str(email_form.cleaned_data['numbers1'])
            numbers2 = str(email_form.cleaned_data['numbers2'])
            return(email,birthday,area_code,numbers1,numbers2)
        else:
            error = 'Age Restriction'
            return error

def clean_create_user_form(request):
    form = createUserForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        birthday = form.cleaned_data['birthday']
        area_code = form.cleaned_data['area_code']
        numbers1 = form.cleaned_data['numbers1']
        numbers2 = form.cleaned_data['numbers2']
        return (username,password,email,birthday,area_code,numbers1,numbers2)
    return False
    raise Exception('clean_create_user_form')

def sort_csv_data(column):
    key = ['event_name', 'date', 'start_time', 'end_time', 'description', 'num_needed', 'activity_level', 'address1', 'address2', 'city', 'state', 'zip_code', 'country', 'business_name', 'baddress1', 'baddress2', 'bcity', 'bstate', 'bzip_code', 'bcountry', 'bphone_number']
    timeslot_dict = {}
    length_of_column = len(column)
    for i in range(length_of_column):
        if column[i] == '':
            timeslot_dict[key[i]] = None
        else:
            timeslot_dict[key[i]] = column[i]
    return timeslot_dict

def sort_request_data(request):
    form = timeslotForm(request.POST)
    if form.is_valid():
        form = form.cleaned_data
        return form
        raise Exception('sort_request_data')  

def delete_user_account(request=None, user_account=None):
    user_account.delete()
    raise Exception('delete_user_account')    

def delete_custom_user(request=None, custom_user=None):
    custom_user.delete()
    raise Exception('delete_custom_user')

def clean0():
    if User.objects.filter(username='jessethomas88'):
        user_account = User.objects.get(username='jessethomas88')
        if CustomUser.objects.filter(user_account=user_account):
            custom_user = CustomUser.objects.get(user_account=user_account)
            custom_user.delete()
        user_account.delete()
    if PhoneNumber.objects.filter(area_code='123',numbers1='456',numbers2='7890'):
        phone_number = PhoneNumber.objects.get(area_code='123',numbers1='456',numbers2=7890)
        phone_number.delete()

def clean1():
    address1 = ['111','222','333','123']
    area_code = ['234']
    numbers1 = ['567']
    numbers2 = ['8901']
    business_name = ['CSV Company']
    if TimeSlot.objects.filter(description='This is from CSV Upload'):
        timeslots = TimeSlot.objects.filter(description='This is from CSV Upload')
        for timeslot in timeslots:
            timeslot.delete()
    for i in business_name:
        if Business.objects.filter(business_name = i):
            business = Business.objects.get(business_name=i)
            business.delete()
    for i in address1:
        if Address.objects.filter(address1 = i):
            address = Address.objects.get(address1 = i)
            address.delete()
    for i in range(len(area_code)):
        if PhoneNumber.objects.filter(
            area_code=area_code[i],
            numbers1=numbers1[i],
            numbers2=numbers2[i]):
            phone_number = PhoneNumber.objects.get(
            area_code=area_code[i],
            numbers1=numbers1[i],
            numbers2=numbers2[i])
            phone_number.delete()

def clean2():
    emails = [
        'tmaek@me.com',
        'jmgomez@yahoo.ca',
        'cmdrgravy@hotmail.com',
        'jsbach@live.com',
        'lbaxter@me.com',
        'tamas@mac.com',
        'pmint@msn.com',
        'munson@icloud.com',
        'krueger@verizon.net',
        'webteam@aol.com',
        'tamas@aol.com',
        'dwheeler@yahoo.com',]
    for i in emails:
        objects = User.objects.filter(email=i)
        for j in objects:
            objects2 = CustomUser.objects.filter(user_account=j)
            for k in objects2:
                k.delete()
            j.delete()

def sendmail(user_account,timeslot,temp_password=0,new_user=False):
    sender = 'jessethomascs@gmail.com'
    email = [user_account.email]
    if new_user:
        send_mail(
            'Volunteer Registration',
            f'''Thank you for registering. Use the following information to login to your account:
            
            Username: {user_account.username}
            Temporary Password: {temp_password}

            Timeslot Information
            Event name: {timeslot.event_name}
            Date: {timeslot.date}
            Time: {timeslot.start_time} to {timeslot.end_time}
            Address: {timeslot.address}

            To log in follow this localhost:8000/login
            ''',
            sender,
            email
        )
    else:
        send_mail(
            'Registration',
            f'''Thank you for registering.

            Timeslot Information
            Event name: {timeslot.event_name}
            Date: {timeslot.date}
            Time: {timeslot.start_time} to {timeslot.end_time}
            Address: {timeslot.address}
            ''',
            sender,
            email
        )

    # if request.method == 'POST':
    #     if loggedIn(request):
    #         if registerLoggedInUser(request, TimeSlot_detail):
    #             return redirect('thanks')
    #         else:
    #             invalid = True
    #             return render(request, 'Registration/detail.html', {'TimeSlot': TimeSlot_detail, 'form':form, 'invalid':invalid})
    #     elif userExists(request):
    #         if registerExistingUser(request, TimeSlot_detail):
    #             return redirect('thanks')
    #         else:
    #             invalid = True
    #             return render(request, 'Registration/detail.html', {'TimeSlot': TimeSlot_detail, 'form':form, 'invalid':invalid})
    #     else:
    #         if registerNewUser(request, TimeSlot_detail):
    #             return redirect('thanks')
    #         else:
    #             invalid = True
    #             return render(request, 'Registration/detail.html', {'TimeSlot': TimeSlot_detail, 'form':form, 'invalid':invalid})
    #{'timeslot': timeslot.display_timeslot, 'form':form, 'invalid':invalid, 'text_area':text_area}
