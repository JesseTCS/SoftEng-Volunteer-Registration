# SoftEng-Volunteer-Registration
A volunteer registration website for Software Engineering

<br>For admin access, run the django server and then go to localhost:8000/admin. Your username is your first name and text me for your temporary password.

<br>To run the django server make sure that django is installed on your computer ( https://www.djangoproject.com/download/ ) and navigate in your terminal to the folder where manage.py is. Run the command 'python3 manage.py runserver' (without quotes).

<br>If you would like to test the email portion of the project go to settings.py and for EMAIL_HOST_USER = 'PutYourEmailHere' and for EMAIL_HOST_PASSWORD = 'YourEmailPassword'. If you are using your personal gmail for testing, you will most likely need to create an app password through your google account.

<br>Todo: <br /> 
[ ] - Register people for specific TimeSlots  <br /> 
   &nbsp;&nbsp;&nbsp;&nbsp;[X] - when register an email is sent out <br /> 
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ ] - increment number of volunteers by one  <br /> 
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ ] - allow corprate user to register groups  <br /> 
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ ] - if number of volunteers have reached the max, remove time slot normal view. Keep in admin/user view.  <br /> 
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; [ ] - if number of volunteer drops back below the max, place the time slot back in normal view.  <br />  <br /> 

[ ] - External TimeSlot manage system <br /> 
   &nbsp;&nbsp;&nbsp;&nbsp; [ ]  - Build User/admin handling system  <br /> 
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ ] - allow admins to input TimeSlots  <br /> 
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[ ] - allow admins to bulk upload with .csv file  <br /> 

Issue:
1) Under Timeslot model superadmins able to set end_time before start time. <br /> 
   &nbsp;&nbsp;&nbsp; -Pending ideas for solution: <br /> 
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1) create a seperate sign in and time management webpage apart from the superadmins login and manage conditional there for quality control.
