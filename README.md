# SoftEng-Volunteer-Registration
A volunteer registration website for Software Engineering

Todo:
[ ] - Register people for specific TimeSlots
    [ ] - when register an email is sent out
        [ ] - increment number of volunteers by one
    [ ] - allow corprate user to register groups
    [ ] - if number of volunteers have reached the max, remove time slot normal view. Keep in admin/user view.
        [ ] - if number of volunteer drops back below the max, place the time slot back in normal view.

[ ] - External TimeSlot manage system
    [ ] - Build User/admin handling system
        [ ] - allow admins to input TimeSlots
        [ ] - allow admins to bulk upload with .csv file

Issue:
1) Under Timeslot model superadmins able to set end_time before start time.
    -Pending ideas for solution:
        1) create a seperate sign in and time management webpage apart from the superadmins login and manage conditional there for quality control.