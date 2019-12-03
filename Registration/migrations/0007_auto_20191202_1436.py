# Generated by Django 2.2.7 on 2019-12-02 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Registration', '0006_timeslot_event_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timeslot',
            name='Event_Name',
            field=models.CharField(default='Event', max_length=100),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='activity_level',
            field=models.CharField(blank=True, choices=[('L', 'Low'), ('M', 'Medium'), ('H', 'High')], max_length=1),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='date_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='end_time',
            field=models.TimeField(auto_now=True),
        ),
    ]
