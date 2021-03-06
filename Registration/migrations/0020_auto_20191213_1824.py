# Generated by Django 2.2.7 on 2019-12-13 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Registration', '0019_auto_20191213_1509'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timeslot',
            old_name='Event_Name',
            new_name='event_name',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='age',
        ),
        migrations.AddField(
            model_name='customuser',
            name='birthday',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='business',
            name='opt_in',
            field=models.ManyToManyField(related_name='opt_in', to='Registration.CustomUser'),
        ),
    ]
